// Read-only view over the PromptingCraft.com knowledge ledger. All guidance text, URLs,
// dates and hashes come from the skill's own files; catalog-index.json only adds search
// facets keyed by ledger ids.
import knowledge from '../../skills/promptingcraft/references/knowledge.json' with { type: 'json' };
import registry from '../../skills/promptingcraft/references/sources.json' with { type: 'json' };
import baseline from '../../sources-baseline.json' with { type: 'json' };
import facets from './catalog-index.json' with { type: 'json' };

export const TARGET_AGENTS = ['codex', 'claude-code', 'cursor', 'chatgpt'];
export const MODEL_FAMILIES = ['openai', 'anthropic'];
export const KINDS = ['model_guidance', 'platform_documentation', 'agent_skills_standard', 'promptingcraft_methodology'];
export const TOPICS = [
  'context-and-structure', 'instruction-hierarchy', 'untrusted-content', 'reasoning', 'structured-output',
  'tool-use', 'evaluation', 'caching-and-cost', 'scope-control', 'long-context', 'skills-and-plugins',
  'agent-workflows', 'planning-and-modes', 'model-selection', 'discovery',
];
// Codex and ChatGPT run OpenAI models; Claude Code runs Claude models. Cursor can run
// several model families, so its model guidance depends on the model_family filter.
const AGENT_MODEL_FAMILY = { codex: 'openai', chatgpt: 'openai', 'claude-code': 'anthropic', cursor: null };
const KIND_ORDER = Object.fromEntries(KINDS.map((kind, i) => [kind, i]));
const REPOSITORY = 'https://gitlab.com/revanalex/promptingcraft-skill';
const LEDGER_PATH = 'skills/promptingcraft/references/knowledge.json';
const REGISTRY_PATH = 'skills/promptingcraft/references/sources.json';
const BASELINE_PATH = 'sources-baseline.json';

const withoutFragment = (url) => url.split('#')[0];
const familyOf = (provider) => (MODEL_FAMILIES.includes(provider) ? provider : null);

function snapshotOf(sourceId) {
  const row = baseline.sources[sourceId];
  if (!row || !row.hash) return { verified_at: null, content_sha256: null };
  return { verified_at: row.last_content_checked_at ?? row.checked_at ?? null, content_sha256: row.hash };
}

const sourceById = new Map(registry.sources.map((source) => [source.id, source]));
const sourceByUrl = new Map(registry.sources.map((source) => [withoutFragment(source.canonical_url), source]));

function sourceSummary(source) {
  return {
    source_id: source.id,
    provider: source.provider,
    canonical_url: source.canonical_url,
    role: source.role,
    applicability: source.applicability,
    verified_snapshot: snapshotOf(source.id),
  };
}

function buildRecords() {
  const records = [];
  const recSources = new Map();
  for (const rec of knowledge.recommendations) {
    const facet = facets.recommendations[rec.id];
    if (!facet) throw new Error(`catalog-index.json lacks recommendation ${rec.id}`);
    const source = sourceByUrl.get(withoutFragment(rec.url));
    if (!source) throw new Error(`No registry source for recommendation ${rec.id}`);
    const topics = recSources.get(source.id) ?? new Set();
    facet.topics.forEach((topic) => topics.add(topic));
    recSources.set(source.id, topics);
    records.push({
      id: rec.id,
      record_type: 'recommendation',
      kind: facet.kind,
      official: true,
      labels: rec.labels,
      scope: rec.labels.includes('MODEL_SPECIFIC') ? 'model_specific' : 'general',
      provider: rec.provider,
      model_family: facet.kind === 'model_guidance' ? familyOf(rec.provider) : null,
      agents: facet.agents ?? [],
      topics: facet.topics,
      title: rec.source_title,
      summary: rec.recommendation,
      detail: {
        recommendation: rec.recommendation,
        applies_to: rec.applicable_model_family,
        apply_when: rec.apply_when,
        evidence_or_limitation: rec.evidence_or_limitation,
        conflicts_with_existing_guidance: rec.conflicts_with_existing_guidance,
        promptingcraft_applicability: rec.promptingcraft_applicability,
        mandatory_for_all_prompts: rec.mandatory_for_all_prompts,
      },
      canonical_url: rec.url,
      retrieval_date: rec.retrieval_date,
      source: sourceSummary(source),
    });
  }
  for (const item of knowledge.promptingcraft_adaptations) {
    const facet = facets.methodology[item.id];
    if (!facet) throw new Error(`catalog-index.json lacks methodology ${item.id}`);
    records.push({
      id: item.id,
      record_type: 'methodology',
      kind: 'promptingcraft_methodology',
      official: false,
      labels: item.labels,
      scope: 'general',
      provider: 'promptingcraft',
      model_family: null,
      agents: [],
      topics: facet.topics,
      title: 'PromptingCraft.com methodology',
      summary: item.recommendation,
      detail: {
        recommendation: item.recommendation,
        evidence: item.evidence,
        limitation: item.limitation,
        status: 'PromptingCraft.com methodology. It is not an official recommendation of OpenAI, Anthropic, Cursor or the Agent Skills project.',
      },
      canonical_url: `${REPOSITORY}/-/blob/main/${LEDGER_PATH}`,
      retrieval_date: null,
      source: null,
    });
  }
  for (const source of registry.sources) {
    if (recSources.has(source.id)) continue;
    const facet = facets.sources[source.id];
    if (!facet) throw new Error(`catalog-index.json lacks source ${source.id}`);
    records.push({
      id: source.id,
      record_type: 'source',
      kind: facet.kind,
      official: true,
      labels: [],
      scope: 'general',
      provider: source.provider,
      model_family: facet.model_family ?? null,
      agents: facet.agents ?? [],
      topics: facet.topics,
      title: source.canonical_url.replace('https://', ''),
      summary: source.applicability,
      detail: { role: source.role, applicability: source.applicability },
      canonical_url: source.canonical_url,
      retrieval_date: null,
      source: sourceSummary(source),
    });
  }
  records.sort((a, b) => KIND_ORDER[a.kind] - KIND_ORDER[b.kind] || a.provider.localeCompare(b.provider) || a.id.localeCompare(b.id));
  return { records, recSourceIds: new Set(recSources.keys()) };
}

const built = buildRecords();
export const RECORDS = built.records;
export const RECORD_IDS = RECORDS.map((record) => record.id);
export const SOURCE_IDS = registry.sources.map((source) => source.id);
export const REC_SOURCE_IDS = built.recSourceIds;
const recordById = new Map(RECORDS.map((record) => [record.id, record]));

export function provenance(ledgerCommit) {
  const commit = /^[0-9a-f]{40}$/.test(ledgerCommit ?? '') ? ledgerCommit : null;
  const ref = commit ?? 'main';
  return {
    ledger_commit: commit,
    ledger_url: `${REPOSITORY}/-/blob/${ref}/${LEDGER_PATH}`,
    registry_url: `${REPOSITORY}/-/blob/${ref}/${REGISTRY_PATH}`,
    snapshot_url: `${REPOSITORY}/-/blob/${ref}/${BASELINE_PATH}`,
    curated_on: knowledge.curated_on ?? null,
    freshness_note: knowledge.freshness,
    label_definitions: knowledge.label_definitions,
  };
}

function summarize(record) {
  const { detail, source, ...rest } = record;
  return { ...rest, verified_at: source?.verified_snapshot.verified_at ?? null };
}

export function search({ target_agent = 'any', model_family = 'any', scope = 'any', topic, kind, limit = 10 }) {
  const notes = [];
  let families = MODEL_FAMILIES;
  if (model_family === 'other') {
    families = [];
    notes.push('No official model guidance is curated for other model families. Platform documentation and the Agent Skills standard can still apply; check the model provider\'s own documentation.');
  } else if (model_family !== 'any') {
    families = [model_family];
  } else if (target_agent !== 'any' && AGENT_MODEL_FAMILY[target_agent]) {
    families = [AGENT_MODEL_FAMILY[target_agent]];
  }
  if (target_agent !== 'any' && model_family !== 'any' && model_family !== 'other') {
    const implied = AGENT_MODEL_FAMILY[target_agent];
    if (implied && implied !== model_family) {
      notes.push(`${target_agent} normally runs ${implied} models; results follow the requested model_family (${model_family}). Confirm the executor model before applying model-specific guidance.`);
    }
  }
  if (target_agent === 'cursor' && model_family === 'any') {
    notes.push('Cursor can run several model families. Pass model_family to include model guidance for the model the Cursor agent will use.');
  }
  const matches = RECORDS.filter((record) => {
    if (kind && record.kind !== kind) return false;
    if (topic && !record.topics.includes(topic)) return false;
    if (scope !== 'any' && record.scope !== scope) return false;
    if (record.kind === 'promptingcraft_methodology') return kind === 'promptingcraft_methodology';
    if (record.kind === 'model_guidance') {
      if (target_agent === 'cursor' && model_family === 'any') return false;
      return record.model_family !== null && families.includes(record.model_family);
    }
    if (target_agent !== 'any') return record.agents.includes(target_agent);
    return true;
  });
  if (!matches.length) notes.push('No curated record matches these filters. Absence here does not mean no official guidance exists.');
  return {
    results: matches.slice(0, limit).map(summarize),
    total_matches: matches.length,
    returned: Math.min(limit, matches.length),
    filters: { target_agent, model_family, scope, topic: topic ?? null, kind: kind ?? null, limit },
    notes,
  };
}

export function getRecord(id) {
  const record = recordById.get(id);
  if (record) return record;
  // A registry source that is the page of a recommendation is returned with those recommendations.
  if (REC_SOURCE_IDS.has(id)) {
    const source = sourceById.get(id);
    return {
      id,
      record_type: 'source',
      kind: RECORDS.find((r) => r.source?.source_id === id)?.kind ?? 'model_guidance',
      official: true,
      labels: [],
      scope: 'general',
      provider: source.provider,
      model_family: familyOf(source.provider),
      agents: [],
      topics: [...new Set(RECORDS.filter((r) => r.source?.source_id === id).flatMap((r) => r.topics))],
      title: source.canonical_url.replace('https://', ''),
      summary: source.applicability,
      detail: { role: source.role, applicability: source.applicability, recommendations: RECORDS.filter((r) => r.source?.source_id === id).map((r) => r.id) },
      canonical_url: source.canonical_url,
      retrieval_date: null,
      source: sourceSummary(source),
    };
  }
  return null;
}

export function sourceRecord(id) {
  const source = sourceById.get(id);
  return source ? { source, policy: registry.policies[source.provider], snapshot: snapshotOf(id) } : null;
}
