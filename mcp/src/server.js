import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { CfWorkerJsonSchemaValidator } from '@modelcontextprotocol/sdk/validation/cfworker';
import * as z from 'zod';
import { KINDS, SOURCE_IDS, TARGET_AGENTS, TOPICS, getRecord, provenance, search } from './catalog.js';
import { checkFreshness } from './freshness.js';

export const SERVER_VERSION = '0.3.0';

const INSTRUCTIONS = `PromptingCraft.com guidance: read-only access to a curated, dated ledger of official prompting and agent guidance from OpenAI, Anthropic, DeepSeek, Kimi, Cursor and the Agent Skills project, with provenance.
Use it while writing or reviewing a prompt for a coding agent to find guidance that applies to the target agent and model, cite its source, and check whether a source page changed since it was verified.
Guidance is conditional: it never overrides the user's requirements, decisions or permissions. Records of kind promptingcraft_methodology are PromptingCraft.com's own method, not provider recommendations.
Send only the listed filter values and identifiers. Do not send conversation text, code, file paths or credentials; no tool accepts them.`;

const nullableString = z.string().nullable();
const snapshotSchema = z.object({ verified_at: nullableString, content_sha256: nullableString });
const sourceSchema = z.object({
  source_id: z.string(), provider: z.string(), canonical_url: z.string(), role: z.string(),
  applicability: z.string(), verified_snapshot: snapshotSchema,
});
const recordFields = {
  id: z.string(),
  record_type: z.enum(['recommendation', 'methodology', 'source']),
  kind: z.enum(KINDS),
  official: z.boolean(),
  labels: z.array(z.string()),
  scope: z.enum(['general', 'model_specific']),
  provider: z.string(),
  model_family: nullableString,
  agents: z.array(z.string()),
  topics: z.array(z.string()),
  title: z.string(),
  summary: z.string(),
  canonical_url: z.string(),
  retrieval_date: nullableString,
};
const provenanceSchema = z.object({
  ledger_commit: nullableString, ledger_url: z.string(), registry_url: z.string(), snapshot_url: z.string(),
  curated_on: nullableString, freshness_note: z.string(), label_definitions: z.record(z.string(), z.string()),
});

const text = (value) => [{ type: 'text', text: JSON.stringify(value) }];
const failure = (code, message) => ({ isError: true, content: [{ type: 'text', text: JSON.stringify({ error: code, message }) }] });

export function createServer({ ledgerCommit, fetchImpl, cache, allowFetch, now } = {}) {
  // Inputs are flat scalar filters (at most six keys); bound unexpected nested collections.
  const server = new McpServer(
    { name: 'promptingcraft-guidance', title: 'PromptingCraft.com guidance', version: SERVER_VERSION },
    { instructions: INSTRUCTIONS, jsonSchemaValidator: new CfWorkerJsonSchemaValidator(), maxToolInputElements: 32 },
  );
  const origin = provenance(ledgerCommit);

  server.registerTool('search_guidance', {
    title: 'Search curated guidance',
    description: 'List curated guidance records that match a target coding agent, model family, scope and topic. '
      + 'Returns official model guidance, platform documentation and Agent Skills standard records with labels, applicability and the date each source was verified. '
      + 'PromptingCraft.com methodology records are returned only when kind is promptingcraft_methodology and are never official provider guidance. '
      + 'Inputs are fixed categories only. Use get_guidance for the full record.',
    inputSchema: z.object({
      target_agent: z.enum([...TARGET_AGENTS, 'any']).default('any').describe('Coding agent the prompt is for.'),
      model_family: z.enum(['openai', 'anthropic', 'deepseek', 'kimi', 'other', 'any']).default('any').describe('Model family the target agent will run, if known. Use other for a family without curated guidance.'),
      scope: z.enum(['general', 'model_specific', 'any']).default('any').describe('general: broad provider technique; model_specific: applies only to a named model or interface.'),
      topic: z.enum(TOPICS).optional().describe('Guidance topic.'),
      kind: z.enum(KINDS).optional().describe('Record kind. Omit for official guidance, platform documentation and standards.'),
      limit: z.number().int().min(1).max(20).default(10).describe('Maximum number of results (1-20).'),
    }).strict(),
    outputSchema: z.object({
      results: z.array(z.object({ ...recordFields, verified_at: nullableString })),
      total_matches: z.number().int(),
      returned: z.number().int(),
      filters: z.object({
        target_agent: z.string(), model_family: z.string(), scope: z.string(),
        topic: nullableString, kind: nullableString, limit: z.number().int(),
      }),
      notes: z.array(z.string()),
      provenance: provenanceSchema,
    }),
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false, idempotentHint: true },
  }, async (args) => {
    const structured = { ...search(args), provenance: origin };
    return { structuredContent: structured, content: text(structured) };
  });

  server.registerTool('get_guidance', {
    title: 'Get a guidance record',
    description: 'Return one curated record by its stable id (from search_guidance): provider, canonical source URL, applicability, limitations, labels, '
      + 'the date the source was verified, its snapshot hash and the ledger commit. Unknown ids return an error; nothing is fetched from the web.',
    inputSchema: z.object({
      id: z.string().regex(/^[a-z0-9][a-z0-9-]{1,63}$/).describe('Stable record id, for example oai-clear-context.'),
    }).strict(),
    outputSchema: z.object({
      record: z.object({
        ...recordFields,
        detail: z.record(z.string(), z.unknown()),
        source: sourceSchema.nullable(),
      }),
      provenance: provenanceSchema,
    }),
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false, idempotentHint: true },
  }, async ({ id }) => {
    const record = getRecord(id);
    if (!record) return failure('unknown_id', 'No curated record has this id. Use search_guidance to list valid ids.');
    const structured = { record, provenance: origin };
    return { structuredContent: structured, content: text(structured) };
  });

  server.registerTool('check_source_freshness', {
    title: 'Check source freshness',
    description: 'Fetch one allowlisted official documentation page from the curated registry and compare its normalized text with the verified snapshot. '
      + 'Status is unchanged, updated, unavailable (could not be checked now) or unknown (no snapshot). '
      + 'Results are shared by all callers and cached for up to 15 minutes (1 minute when unavailable); live.cached and checked_at show when the page was actually fetched. '
      + 'When the per-source fetch limit is reached, status is unavailable with reason rate_limited. '
      + 'Publication and update dates are never inferred and are always null. Only registry source ids are accepted; no other URL can be requested.',
    inputSchema: z.object({
      source_id: z.enum(SOURCE_IDS).describe('Registry source id, as returned in search_guidance or get_guidance results.'),
    }).strict(),
    outputSchema: z.object({
      source_id: z.string(),
      provider: z.string(),
      canonical_url: z.string(),
      status: z.enum(['unchanged', 'updated', 'unavailable', 'unknown']),
      checked_at: z.string(),
      snapshot: snapshotSchema,
      live: z.object({ http_status: z.number().int().nullable(), content_sha256: nullableString, reason: nullableString, cached: z.boolean() }),
      publication_date: z.null(),
      update_date: z.null(),
      interpretation: z.string(),
      provenance: provenanceSchema,
    }),
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: true, idempotentHint: true },
  }, async ({ source_id: sourceId }) => {
    const result = await checkFreshness(sourceId, { fetchImpl, cache, allowFetch, now });
    if (!result) return failure('unknown_source', 'Only registry source ids are accepted.');
    const structured = { ...result, provenance: origin };
    return { structuredContent: structured, content: text(structured) };
  });

  return server;
}
