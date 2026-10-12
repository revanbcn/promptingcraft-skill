// PromptingCraft.com guidance MCP server (Cloudflare Worker, stateless Streamable HTTP).
// Privacy: request bodies are parsed only to answer the call. Nothing is logged or stored,
// except freshness results for public pages, which are cached for FRESHNESS_TTL seconds.
import { WebStandardStreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/webStandardStreamableHttp.js';
import { createServer, SERVER_VERSION } from './server.js';

export const MAX_BODY_BYTES = 65_536;
const FRESHNESS_TTL = 900;
const CACHE_ORIGIN = 'https://mcp.promptingcraft.com/__freshness/';
const SECURITY_HEADERS = {
  'Cache-Control': 'no-store',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'no-referrer',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Expose-Headers': 'Mcp-Session-Id, Mcp-Protocol-Version',
};
const CORS_PREFLIGHT = {
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Accept, Mcp-Protocol-Version, Mcp-Session-Id',
  'Access-Control-Max-Age': '86400',
};

const withHeaders = (response, extra = {}) => {
  const headers = new Headers(response.headers);
  for (const [key, value] of Object.entries({ ...SECURITY_HEADERS, ...extra })) headers.set(key, value);
  return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
};
const plain = (body, status = 200, extra = {}) =>
  withHeaders(new Response(body, { status, headers: { 'Content-Type': 'text/plain; charset=utf-8' } }), extra);
const rpcError = (status, code, message) =>
  withHeaders(new Response(JSON.stringify({ jsonrpc: '2.0', error: { code, message }, id: null }), {
    status, headers: { 'Content-Type': 'application/json' },
  }));

async function readBody(request) {
  const declared = Number(request.headers.get('content-length') ?? '0');
  if (declared > MAX_BODY_BYTES) return { tooLarge: true };
  const bytes = new Uint8Array(await request.arrayBuffer());
  if (bytes.byteLength > MAX_BODY_BYTES) return { tooLarge: true };
  try {
    return { json: JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes)) };
  } catch {
    return { invalid: true };
  }
}

function freshnessCache() {
  const store = globalThis.caches?.default;
  if (!store) return undefined;
  const key = (id) => new Request(`${CACHE_ORIGIN}${encodeURIComponent(id)}`);
  return {
    async get(id) {
      const hit = await store.match(key(id));
      return hit ? hit.json() : null;
    },
    async put(id, value) {
      await store.put(key(id), new Response(JSON.stringify(value), {
        headers: { 'Content-Type': 'application/json', 'Cache-Control': `public, max-age=${FRESHNESS_TTL}` },
      }));
    },
  };
}

export async function handleMcp(request, env, deps = {}) {
  if (request.method === 'OPTIONS') return withHeaders(new Response(null, { status: 204 }), CORS_PREFLIGHT);
  if (request.method !== 'POST') return rpcError(405, -32000, 'Method not allowed: this stateless server accepts POST only.');
  const limiter = env.REQUEST_LIMITER;
  if (limiter) {
    const { success } = await limiter.limit({ key: request.headers.get('cf-connecting-ip') ?? 'unknown' });
    if (!success) return withHeaders(rpcError(429, -32000, 'Rate limit exceeded. Retry in a minute.'), { 'Retry-After': '60' });
  }
  const body = await readBody(request);
  if (body.tooLarge) return rpcError(413, -32600, 'Request body too large.');
  if (body.invalid) return rpcError(400, -32700, 'Parse error: body must be UTF-8 JSON.');

  const fetchLimiter = env.FETCH_LIMITER;
  const server = createServer({
    ledgerCommit: env.LEDGER_COMMIT,
    fetchImpl: deps.fetchImpl,
    cache: deps.cache ?? freshnessCache(),
    allowFetch: fetchLimiter ? async (id) => (await fetchLimiter.limit({ key: `source:${id}` })).success : undefined,
  });
  const transport = new WebStandardStreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
  await server.connect(transport);
  try {
    return withHeaders(await transport.handleRequest(request, { parsedBody: body.json }));
  } finally {
    await server.close();
  }
}

export async function routeRequest(request, env) {
  const { pathname } = new URL(request.url);
  if (pathname === '/mcp') return handleMcp(request, env);
  if (pathname === '/.well-known/openai-apps-challenge') {
    const token = (env.OPENAI_APPS_CHALLENGE ?? '').trim();
    return token ? plain(token) : plain('Not found', 404);
  }
  if (pathname === '/' && request.method === 'GET') {
    return plain(`PromptingCraft.com guidance MCP server ${SERVER_VERSION}\n`
      + 'Streamable HTTP endpoint: https://mcp.promptingcraft.com/mcp (POST, no account needed)\n'
      + 'Tools: search_guidance, get_guidance, check_source_freshness (read-only)\n'
      + 'Docs: https://promptingcraft.com/docs  Privacy: https://promptingcraft.com/privacy\n'
      + 'Developed by the dondego.com team.\n');
  }
  return plain('Not found', 404);
}
