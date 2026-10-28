import { test } from 'node:test';
import assert from 'node:assert/strict';
import worker from '../src/index.js';
import { handleMcp } from '../src/http.js';
import { COMMIT, callTool, htmlPage, rpc } from './helpers.js';

const INIT = { protocolVersion: '2025-06-18', capabilities: {}, clientInfo: { name: 'test', version: '1' } };

test('initialize and tools/list expose three read-only tools with schemas and annotations', async () => {
  const init = await rpc('initialize', INIT);
  assert.equal(init.status, 200);
  assert.equal(init.body.result.serverInfo.name, 'promptingcraft-guidance');
  assert.match(init.body.result.instructions, /not provider recommendations/);
  assert.equal(init.headers.get('mcp-session-id'), null);
  const { body } = await rpc('tools/list', {});
  const tools = Object.fromEntries(body.result.tools.map((t) => [t.name, t]));
  assert.deepEqual(Object.keys(tools).sort(), ['check_source_freshness', 'get_guidance', 'search_guidance']);
  for (const tool of Object.values(tools)) {
    assert.equal(tool.annotations.readOnlyHint, true);
    assert.equal(tool.annotations.destructiveHint, false);
    assert.equal(typeof tool.annotations.openWorldHint, 'boolean');
    assert.equal(tool.inputSchema.additionalProperties, false);
    assert.equal(tool.outputSchema.type, 'object');
    for (const [name, prop] of Object.entries(tool.inputSchema.properties)) {
      if (prop.type === 'string') assert.ok(prop.enum || prop.pattern, `${tool.name}.${name} must be constrained`);
    }
  }
  assert.equal(tools.search_guidance.annotations.openWorldHint, false);
  assert.equal(tools.get_guidance.annotations.openWorldHint, false);
  assert.equal(tools.check_source_freshness.annotations.openWorldHint, true);
  // The description states the shared cache and the per-source fetch limit the tool applies.
  assert.match(tools.check_source_freshness.description, /cached for up to 15 minutes/);
  assert.match(tools.check_source_freshness.description, /rate_limited/);
});

test('tool calls return structured content matching the text content', async () => {
  const search = await callTool('search_guidance', { target_agent: 'claude-code', topic: 'context-and-structure' });
  assert.ok(!search.result.isError);
  assert.deepEqual(JSON.parse(search.result.content[0].text), search.result.structuredContent);
  assert.equal(search.result.structuredContent.provenance.ledger_commit, COMMIT);
  const get = await callTool('get_guidance', { id: 'claude-sonnet-scope' });
  const record = get.result.structuredContent.record;
  assert.equal(record.provider, 'anthropic');
  assert.ok(record.labels.includes('MODEL_SPECIFIC'));
  assert.match(record.source.verified_snapshot.content_sha256, /^[0-9a-f]{64}$/);
  assert.match(get.result.structuredContent.provenance.ledger_url, new RegExp(`/-/blob/${COMMIT}/`));
});

test('invalid, unknown and free-text inputs are rejected predictably', async () => {
  const unknown = await callTool('get_guidance', { id: 'no-such-record' });
  assert.equal(unknown.result.isError, true);
  assert.equal(JSON.parse(unknown.result.content[0].text).error, 'unknown_id');
  for (const [name, args] of [
    ['get_guidance', { id: '../etc/passwd' }],
    ['get_guidance', { id: 'oai-tools', prompt: 'my private task text' }],
    ['search_guidance', { query: 'free text search' }],
    ['search_guidance', { target_agent: 'gemini-cli' }],
    ['search_guidance', { limit: 500 }],
    ['check_source_freshness', { source_id: 'https://evil.example/x' }],
    ['check_source_freshness', { url: 'https://developers.openai.com/api/x' }],
  ]) {
    const response = await callTool(name, args);
    assert.ok(response.result?.isError || response.error, `${name} ${JSON.stringify(args)}`);
  }
});

test('freshness tool reports status without dates and never exposes request data', async () => {
  const fetchImpl = async () => htmlPage(`<main>${'New official text for coding agents with many words in it. '.repeat(3)}</main>`);
  const response = await callTool('check_source_freshness', { source_id: 'cursor-prompting' }, { deps: { fetchImpl } });
  const result = response.result.structuredContent;
  assert.equal(result.status, 'updated');
  assert.equal(result.publication_date, null);
  assert.equal(result.update_date, null);
  assert.ok(!JSON.stringify(result).includes('cf-connecting-ip'));
});

test('HTTP surface: POST only, bounded bodies, parse errors, rate limits, CORS and challenge', async () => {
  const env = { LEDGER_COMMIT: COMMIT };
  const get = await handleMcp(new Request('https://x/mcp'), env);
  assert.equal(get.status, 405);
  const big = await handleMcp(new Request('https://x/mcp', { method: 'POST', body: 'x'.repeat(70_000) }), env);
  assert.equal(big.status, 413);
  const chunked = new ReadableStream({ start(c) { for (let i = 0; i < 20; i += 1) c.enqueue(new Uint8Array(4096)); c.close(); } });
  const streamed = await handleMcp(new Request('https://x/mcp', { method: 'POST', body: chunked, duplex: 'half' }), env);
  assert.equal(streamed.status, 413, 'a streamed body without Content-Length is still capped');
  const spoofed = await handleMcp(new Request('https://x/mcp', { method: 'POST', headers: { 'content-length': 'abc' }, body: '{}' }), env);
  assert.equal(spoofed.status, 413);
  const batched = await handleMcp(new Request('https://x/mcp', { method: 'POST', body: JSON.stringify([{ jsonrpc: '2.0', id: 1, method: 'tools/list' }]) }), env);
  assert.equal(batched.status, 400);
  assert.equal((await batched.json()).error.code, -32600);
  const bad = await handleMcp(new Request('https://x/mcp', { method: 'POST', body: '{not json' }), env);
  assert.equal(bad.status, 400);
  assert.equal((await bad.json()).error.code, -32700);
  const limited = await rpc('tools/list', {}, { env: { REQUEST_LIMITER: { limit: async () => ({ success: false }) } } });
  assert.equal(limited.status, 429);
  assert.equal(limited.headers.get('retry-after'), '60');
  const preflight = await handleMcp(new Request('https://x/mcp', { method: 'OPTIONS' }), env);
  assert.equal(preflight.status, 204);
  assert.match(preflight.headers.get('access-control-allow-headers'), /Mcp-Protocol-Version/);
  assert.equal((await worker.fetch(new Request('https://x/.well-known/openai-apps-challenge'), {})).status, 404);
  const challenge = await worker.fetch(new Request('https://x/.well-known/openai-apps-challenge'), { OPENAI_APPS_CHALLENGE: ' tok_123 ' });
  assert.equal(await challenge.text(), 'tok_123');
  assert.match(challenge.headers.get('content-type'), /^text\/plain/);
  assert.equal((await worker.fetch(new Request('https://x/anything'), {})).status, 404);
  assert.match(await (await worker.fetch(new Request('https://x/'), {})).text(), /dondego\.com team/);
});

test('handling a request writes nothing to the console', async () => {
  const methods = ['log', 'info', 'warn', 'error', 'debug'];
  const original = Object.fromEntries(methods.map((m) => [m, console[m]]));
  const calls = [];
  for (const m of methods) console[m] = (...args) => calls.push([m, args]);
  try {
    await callTool('search_guidance', { target_agent: 'codex' });
    await callTool('get_guidance', { id: 'unknown-id' });
    await callTool('search_guidance', { query: 'secret task text' });
  } finally {
    Object.assign(console, original);
  }
  assert.deepEqual(calls, []);
});

// Field names observed from ChatGPT and Codex in October 2026 (values here are fake).
const HOST_META = {
  'openai/subject': 'subj-FAKE-123', 'openai/session': 'sess-FAKE-456', 'openai/organization': 'org-FAKE',
  'openai/request_id': 'req-FAKE', 'openai/locale': 'es-ES',
  'openai/userLocation': { city: 'FakeCity', region: 'FakeRegion', country: 'ZZ', timezone: 'Etc/Fake', latitude: '12.3456', longitude: '-65.4321' },
  callId: 'call-FAKE', itemId: 'item-FAKE', sessionId: 'sid-FAKE', windowId: 'win-FAKE', threadId: 'thr-FAKE', plugin_id: 'plg-FAKE',
  progressToken: 7, traceparent: '00-FAKE-01',
  'x-codex-turn-metadata': { model: 'fake-model', session_id: 'cx-FAKE', turn_id: 'turn-FAKE', sandbox: 'read-only', turn_started_at_unix_ms: 1 },
};
const metaValues = (value) => (value && typeof value === 'object' ? Object.values(value).flatMap(metaValues) : [String(value)]);

test('host metadata is ignored: same answer, never echoed, nothing logged', async () => {
  const methods = ['log', 'info', 'warn', 'error', 'debug'];
  const original = Object.fromEntries(methods.map((m) => [m, console[m]]));
  const logged = [];
  for (const m of methods) console[m] = (...args) => logged.push(args);
  try {
    for (const [name, args] of [['search_guidance', { target_agent: 'codex' }], ['get_guidance', { id: 'oai-tools' }], ['get_guidance', { id: 'no-such-record' }]]) {
      const plain = await rpc('tools/call', { name, arguments: args });
      const withMeta = await rpc('tools/call', { name, arguments: args, _meta: HOST_META });
      assert.deepEqual(withMeta.body, plain.body, `${name} result must not depend on host metadata`);
      const text = JSON.stringify(withMeta.body);
      for (const value of metaValues(HOST_META).filter((v) => v.length > 2)) assert.ok(!text.includes(value), `${name} echoed metadata value ${value}`);
    }
  } finally {
    Object.assign(console, original);
  }
  assert.deepEqual(logged, []);
});

test('identifying headers do not change or appear in the answer', async () => {
  const headers = { 'x-openai-subject': 'subj-FAKE-H', 'x-openai-session': 'sess-FAKE-H', 'x-forwarded-for': '198.51.100.7', 'cf-connecting-ip': '198.51.100.8', 'cf-ipcountry': 'ZZ' };
  const plain = await rpc('tools/call', { name: 'get_guidance', arguments: { id: 'claude-clear' } });
  const withHeaders = await rpc('tools/call', { name: 'get_guidance', arguments: { id: 'claude-clear' } }, { headers });
  assert.deepEqual(withHeaders.body, plain.body);
  for (const value of Object.values(headers)) assert.ok(!JSON.stringify(withHeaders.body).includes(value));
});

test('model-specific additions are discoverable through the MCP tool schema', async () => {
  for (const family of ['deepseek', 'kimi']) {
    const response = await callTool('search_guidance', { target_agent: 'cursor', model_family: family, topic: 'tool-use' });
    assert.ok(!response.result.isError);
    const record = response.result.structuredContent.results.find((item) => item.model_family === family);
    assert.ok(record, family);
    const detail = await callTool('get_guidance', { id: record.id });
    assert.equal(detail.result.structuredContent.record.provider, family);
    assert.match(detail.result.structuredContent.record.source.verified_snapshot.content_sha256, /^[a-f0-9]{64}$/);
  }
});

test('oversized tool argument collections are rejected before schema validation', async () => {
  const oversized = await callTool('get_guidance', { id: Array(200).fill('x') });
  assert.equal(oversized.result?.isError, true);
  assert.match(oversized.result.content[0].text, /arguments contain more than the maximum of 32 elements/i);
  const valid = await callTool('get_guidance', { id: 'oai-tools' });
  assert.ok(!valid.result?.isError);
});
