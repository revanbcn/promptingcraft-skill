import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { KINDS, RECORDS, REC_SOURCE_IDS, TARGET_AGENTS, TOPICS, getRecord, search } from '../src/catalog.js';

const read = (path) => JSON.parse(readFileSync(new URL(path, import.meta.url), 'utf8'));
const knowledge = read('../../skills/promptcraft/references/knowledge.json');
const registry = read('../../skills/promptcraft/references/sources.json');
const index = read('../src/catalog-index.json');

test('the facet index covers exactly the ledger and holds no guidance text', () => {
  assert.deepEqual(Object.keys(index.recommendations).sort(), knowledge.recommendations.map((r) => r.id).sort());
  assert.deepEqual(Object.keys(index.methodology).sort(), knowledge.promptcraft_adaptations.map((r) => r.id).sort());
  const plainSources = registry.sources.map((s) => s.id).filter((id) => !REC_SOURCE_IDS.has(id)).sort();
  assert.deepEqual(Object.keys(index.sources).sort(), plainSources);
  for (const group of ['recommendations', 'methodology', 'sources']) {
    for (const [id, facet] of Object.entries(index[group])) {
      assert.deepEqual(Object.keys(facet).filter((k) => !['kind', 'topics', 'agents', 'model_family'].includes(k)), [], id);
      assert.ok(facet.topics.length && facet.topics.every((t) => TOPICS.includes(t)), id);
      if (facet.kind) assert.ok(KINDS.includes(facet.kind) && facet.kind !== 'promptcraft_methodology', id);
      for (const agent of facet.agents ?? []) assert.ok(TARGET_AGENTS.includes(agent), id);
    }
  }
});

test('records keep ledger text, labels and provenance unchanged', () => {
  for (const rec of knowledge.recommendations) {
    const record = getRecord(rec.id);
    assert.equal(record.summary, rec.recommendation);
    assert.deepEqual(record.labels, rec.labels);
    assert.equal(record.canonical_url, rec.url);
    assert.equal(record.retrieval_date, rec.retrieval_date);
    assert.equal(record.official, true);
    assert.equal(record.scope, rec.labels.includes('MODEL_SPECIFIC') ? 'model_specific' : 'general');
    assert.ok(record.source.canonical_url.startsWith('https://'));
  }
});

test('methodology is never labelled official provider guidance', () => {
  const methodology = RECORDS.filter((r) => r.kind === 'promptcraft_methodology');
  assert.ok(methodology.length >= 1);
  for (const record of methodology) {
    assert.equal(record.official, false);
    assert.ok(!record.labels.includes('OFFICIAL'));
    assert.match(record.detail.status, /not an official recommendation/);
  }
  for (const record of RECORDS.filter((r) => r.official)) assert.notEqual(record.kind, 'promptcraft_methodology');
  assert.ok(RECORDS.filter((r) => r.provider === 'agentskills').every((r) => r.kind === 'agent_skills_standard'));
  assert.ok(RECORDS.filter((r) => r.provider === 'cursor').every((r) => r.kind === 'platform_documentation'));
});

test('target agents select their model family and platform documentation', () => {
  const codex = search({ target_agent: 'codex', limit: 20 });
  assert.ok(codex.results.length > 0);
  for (const r of codex.results) {
    if (r.kind === 'model_guidance') assert.equal(r.model_family, 'openai');
    else assert.ok(r.agents.includes('codex'), r.id);
  }
  const claude = search({ target_agent: 'claude-code', kind: 'model_guidance', limit: 20 });
  assert.ok(claude.results.length > 0 && claude.results.every((r) => r.model_family === 'anthropic'));
  const cursor = search({ target_agent: 'cursor', limit: 20 });
  assert.ok(cursor.results.every((r) => r.kind !== 'model_guidance'));
  assert.ok(cursor.notes.some((n) => /several model families/.test(n)));
  const cursorClaude = search({ target_agent: 'cursor', model_family: 'anthropic', limit: 20 });
  assert.ok(cursorClaude.results.some((r) => r.model_family === 'anthropic'));
  assert.ok(cursorClaude.results.every((r) => r.kind !== 'model_guidance' || r.model_family === 'anthropic'));
});

test('unknown model families get no invented guidance and an explicit note', () => {
  const other = search({ model_family: 'other', kind: 'model_guidance' });
  assert.equal(other.total_matches, 0);
  assert.ok(other.notes.some((n) => /No official model guidance is curated/.test(n)));
  assert.ok(other.notes.some((n) => /Absence here does not mean/.test(n)));
});

test('scope, topic, kind and limit filters are exact', () => {
  const specific = search({ scope: 'model_specific', limit: 20 });
  assert.ok(specific.results.length > 0 && specific.results.every((r) => r.labels.includes('MODEL_SPECIFIC')));
  const tools = search({ topic: 'tool-use', limit: 20 });
  assert.ok(tools.results.every((r) => r.topics.includes('tool-use')));
  assert.equal(search({ limit: 1 }).returned, 1);
  assert.ok(search({}).results.every((r) => r.kind !== 'promptcraft_methodology'));
  assert.ok(search({ kind: 'promptcraft_methodology' }).results.every((r) => r.official === false));
  const conflict = search({ target_agent: 'codex', model_family: 'anthropic' });
  assert.ok(conflict.notes.some((n) => /normally runs openai models/.test(n)));
});
