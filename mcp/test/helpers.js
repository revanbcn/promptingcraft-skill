import { handleMcp } from '../src/http.js';

export const COMMIT = 'a'.repeat(40);
export const memoryCache = () => {
  const store = new Map();
  return { store, get: async (id) => store.get(id) ?? null, put: async (id, value) => { store.set(id, value); } };
};

export async function rpc(method, params, { env = {}, deps = {}, headers = {} } = {}) {
  const request = new Request('https://mcp.promptingcraft.com/mcp', {
    method: 'POST',
    headers: { 'content-type': 'application/json', accept: 'application/json, text/event-stream', ...headers },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params }),
  });
  const response = await handleMcp(request, { LEDGER_COMMIT: COMMIT, ...env }, { cache: memoryCache(), ...deps });
  const text = await response.text();
  return { status: response.status, headers: response.headers, body: text ? JSON.parse(text) : null };
}

export const callTool = async (name, args, options) => (await rpc('tools/call', { name, arguments: args }, options)).body;

export function htmlPage(body, { contentType = 'text/html; charset=utf-8', status = 200, headers = {} } = {}) {
  return new Response(body, { status, headers: { 'content-type': contentType, ...headers } });
}
