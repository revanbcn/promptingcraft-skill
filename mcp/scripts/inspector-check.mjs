#!/usr/bin/env node
// Protocol checks through MCP Inspector CLI (pinned) against a running server.
// Usage: node scripts/inspector-check.mjs <server-url> <output-dir>
// Writes one JSON file per case plus summary.json; exits 1 if an expectation fails.
import { spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const [url, out] = process.argv.slice(2);
if (!url || !out) {
  console.error('usage: inspector-check.mjs <server-url> <output-dir>');
  process.exit(2);
}
mkdirSync(out, { recursive: true });
const INSPECTOR = '@modelcontextprotocol/inspector@2.8.0';

function inspector(args) {
  const run = spawnSync('npx', ['-y', INSPECTOR, '--cli', url, '--transport', 'http', ...args], { encoding: 'utf8', timeout: 120_000 });
  const stdout = run.stdout.trim();
  let json = null;
  try { json = JSON.parse(stdout); } catch { /* not JSON: an error message */ }
  return { exit: run.status, json, text: json ? null : `${stdout}\n${run.stderr.split('\n').filter((l) => !l.startsWith('npm warn')).join('\n')}`.trim() };
}
const call = (tool, args) => inspector(['--method', 'tools/call', '--tool-name', tool, ...Object.entries(args).flatMap(([k, v]) => ['--tool-arg', `${k}=${v}`])]);
const structured = (r) => r.json?.structuredContent ?? null;
const isError = (r) => r.exit !== 0 || r.json?.isError === true;

const cases = [
  ['tools-list', () => inspector(['--method', 'tools/list']), (r) => {
    const tools = r.json?.tools ?? [];
    return tools.length === 3 && tools.every((t) => t.annotations?.readOnlyHint === true && t.annotations?.destructiveHint === false
      && typeof t.annotations?.openWorldHint === 'boolean' && t.outputSchema && t.inputSchema?.additionalProperties === false);
  }],
  ['search-codex-tool-use', () => call('search_guidance', { target_agent: 'codex', topic: 'tool-use' }),
    (r) => structured(r)?.results.length > 0 && structured(r).results.every((x) => x.kind !== 'model_guidance' || x.model_family === 'openai')],
  ['search-claude-code', () => call('search_guidance', { target_agent: 'claude-code' }),
    (r) => structured(r)?.results.some((x) => x.model_family === 'anthropic')],
  ['search-cursor-any-model', () => call('search_guidance', { target_agent: 'cursor' }),
    (r) => structured(r)?.results.every((x) => x.kind !== 'model_guidance') && structured(r).notes.length > 0],
  ['search-unknown-model-family', () => call('search_guidance', { model_family: 'other', kind: 'model_guidance' }),
    (r) => structured(r)?.total_matches === 0 && structured(r).notes.some((n) => /No official model guidance is curated/.test(n))],
  ['search-methodology', () => call('search_guidance', { kind: 'promptcraft_methodology' }),
    (r) => structured(r)?.results.length > 0 && structured(r).results.every((x) => x.official === false)],
  ['get-recommendation', () => call('get_guidance', { id: 'oai-untrusted-data' }),
    (r) => structured(r)?.record.provider === 'openai' && /^[0-9a-f]{64}$/.test(structured(r).record.source.verified_snapshot.content_sha256)
      && /^[0-9a-f]{40}$/.test(structured(r).provenance.ledger_commit ?? '')],
  ['get-methodology', () => call('get_guidance', { id: 'contract-provenance' }),
    (r) => structured(r)?.record.official === false && /not an official recommendation/.test(structured(r).record.detail.status)],
  ['get-unknown-id', () => call('get_guidance', { id: 'no-such-record' }), (r) => isError(r)],
  ['invalid-target-agent', () => call('search_guidance', { target_agent: 'gemini-cli' }), (r) => isError(r)],
  ['private-looking-free-text', () => call('search_guidance', { query: 'Fix /Users/alice/app/.env API_KEY=sk-test-123' }), (r) => isError(r)],
  ['private-looking-id', () => call('get_guidance', { id: '/Users/alice/secret.txt' }), (r) => isError(r)],
  ['unsupported-source-url', () => call('check_source_freshness', { source_id: 'https://example.com/docs' }), (r) => isError(r)],
  ['freshness-openai-guide', () => call('check_source_freshness', { source_id: 'oai-clear-context' }),
    (r) => ['unchanged', 'updated', 'unavailable'].includes(structured(r)?.status) && structured(r).publication_date === null && structured(r).update_date === null],
  ['freshness-claude-evaluations', () => call('check_source_freshness', { source_id: 'claude-evaluations' }),
    (r) => ['unchanged', 'updated', 'unavailable'].includes(structured(r)?.status) && structured(r).update_date === null],
  ['freshness-cursor-prompting', () => call('check_source_freshness', { source_id: 'cursor-prompting' }),
    (r) => ['unchanged', 'updated', 'unavailable'].includes(structured(r)?.status)],
];

const summary = [];
for (const [name, run, expect] of cases) {
  const result = run();
  const pass = Boolean(expect(result));
  writeFileSync(join(out, `${name}.json`), `${JSON.stringify(result, null, 2)}\n`);
  const s = structured(result);
  summary.push({ case: name, pass, exit: result.exit, error: isError(result), status: s?.status ?? null, reason: s?.live?.reason ?? null, results: s?.results?.length ?? null });
  console.log(`${pass ? 'PASS' : 'FAIL'} ${name}${s?.status ? ` (${s.status}${s.live?.reason ? `: ${s.live.reason}` : ''})` : ''}`);
}
writeFileSync(join(out, 'summary.json'), `${JSON.stringify({ inspector: INSPECTOR, server: url, cases: summary }, null, 2)}\n`);
process.exit(summary.every((c) => c.pass) ? 0 : 1);
