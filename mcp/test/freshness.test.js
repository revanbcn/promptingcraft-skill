import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { allowedUrl, checkFreshness } from '../src/freshness.js';
import { htmlPage, memoryCache } from './helpers.js';

const registry = JSON.parse(readFileSync(new URL('../../skills/promptcraft/references/sources.json', import.meta.url), 'utf8'));
const openai = registry.policies.openai;
const ID = 'codex-prompting';
const URL0 = registry.sources.find((s) => s.id === ID).canonical_url;
const page = `<main>${'Changed official guidance text for a coding agent with enough words to count. '.repeat(3)}</main>`;
const now = () => new Date('2026-10-13T10:00:00.000Z');

test('URL policy mirrors scripts/freshness.py', () => {
  assert.ok(allowedUrl('https://developers.openai.com/api/docs/guides/x', openai));
  for (const bad of [
    'http://developers.openai.com/api/x', 'https://evil.example/api/x', 'https://developers.openai.com/other',
    'https://developers.openai.com/api/x?q=1', 'https://developers.openai.com/api/x#f', 'https://developers.openai.com/api/%2e%2e/x',
    'https://developers.openai.com/api/../x', 'https://user@developers.openai.com/api/x', 'https://developers.openai.com:8443/api/x',
  ]) assert.equal(allowedUrl(bad, openai), false, bad);
});

test('a page whose text differs from the snapshot is updated, with no invented dates', async () => {
  const seen = [];
  const result = await checkFreshness(ID, { now, fetchImpl: async (url, init) => { seen.push([url, init.redirect]); return htmlPage(page); } });
  assert.equal(result.status, 'updated');
  assert.equal(result.publication_date, null);
  assert.equal(result.update_date, null);
  assert.match(result.live.content_sha256, /^[0-9a-f]{64}$/);
  assert.notEqual(result.live.content_sha256, result.snapshot.content_sha256);
  assert.equal(result.checked_at, '2026-10-13T10:00:00Z');
  assert.deepEqual(seen, [[URL0, 'manual']]);
});

test('redirects are followed only inside the provider policy', async () => {
  const inside = await checkFreshness(ID, { now, fetchImpl: async (url) => (url === URL0
    ? new Response(null, { status: 301, headers: { location: '/docs/prompting-v2' } }) : htmlPage(page)) });
  assert.equal(inside.status, 'updated');
  for (const location of ['https://evil.example/docs/x', '//evil.example/docs/x', 'http://learn.chatgpt.com/docs/x', '/elsewhere/x']) {
    const outside = await checkFreshness(ID, { now, fetchImpl: async () => new Response(null, { status: 302, headers: { location } }) });
    assert.equal(outside.status, 'unavailable', location);
    assert.equal(outside.live.reason, 'redirect_outside_policy', location);
  }
  let hops = 0;
  const loop = await checkFreshness(ID, { now, fetchImpl: async () => { hops += 1; return new Response(null, { status: 307, headers: { location: URL0 } }); } });
  assert.equal(loop.live.reason, 'too_many_redirects');
  assert.equal(hops, 5);
});

test('failures are unavailable with a reason, never a guess', async () => {
  const cases = [
    [async () => htmlPage('gone', { status: 404 }), 'http_404'],
    [async () => { const e = new Error('t'); e.name = 'TimeoutError'; throw e; }, 'timeout'],
    [async () => { throw new TypeError('dns'); }, 'network_error'],
    [async () => htmlPage(`<main>Just a moment... ${'checking '.repeat(30)}</main>`), 'access_challenge'],
    [async () => htmlPage('x'.repeat(1_048_577), { contentType: 'text/plain' }), 'response_too_large'],
    [async () => htmlPage('{}', { contentType: 'application/json' }), 'unsupported_content_type'],
  ];
  for (const [fetchImpl, reason] of cases) {
    const result = await checkFreshness(ID, { now, fetchImpl });
    assert.equal(result.status, 'unavailable', reason);
    assert.equal(result.live.reason, reason);
    assert.equal(result.live.content_sha256, null);
    assert.match(result.interpretation, /dated cached guidance/);
  }
});

test('results are cached, and the outbound limiter is honoured', async () => {
  const cache = memoryCache();
  let calls = 0;
  const fetchImpl = async () => { calls += 1; return htmlPage(page); };
  const first = await checkFreshness(ID, { now, fetchImpl, cache });
  const second = await checkFreshness(ID, { now, fetchImpl, cache });
  assert.equal(calls, 1);
  assert.equal(first.live.cached, false);
  assert.equal(second.live.cached, true);
  assert.equal(second.checked_at, first.checked_at);
  const limited = await checkFreshness('cursor-prompting', { now, fetchImpl, cache, allowFetch: async () => false });
  assert.equal(limited.status, 'unavailable');
  assert.equal(limited.live.reason, 'rate_limited');
  assert.equal(calls, 1);
  assert.equal(await checkFreshness('not-a-source', { now, fetchImpl }), null);
});
