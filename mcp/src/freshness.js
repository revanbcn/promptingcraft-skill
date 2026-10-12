// Compares an allowlisted official source with the verified snapshot in
// sources-baseline.json, using the same URL policy and text normalization as
// scripts/freshness.py. Read-only; never infers publication or update dates.
import { MAX_BYTES, NormalizeError, normalize, sha256Hex } from './normalize.js';
import { sourceRecord } from './catalog.js';

// One deadline for the whole check, redirects included.
export const FETCH_TIMEOUT_MS = 12_000;
const MAX_REDIRECTS = 4;
const REDIRECT_STATUSES = new Set([301, 302, 303, 307, 308]);
const HEADERS = {
  'User-Agent': 'PromptingCraft.com-docs-check/0.3 (+https://promptingcraft.com; public read-only)',
  Accept: 'text/markdown,text/plain,text/html',
  'Accept-Encoding': 'identity',
};

// Mirrors validate_url() in scripts/freshness.py (DNS resolution is left to the platform).
export function allowedUrl(url, policy) {
  if (typeof url !== 'string' || url.length > 2048 || url.includes('\\') || /[\x00-\x20]/.test(url)) return false;
  let parsed;
  try {
    parsed = new URL(url);
  } catch {
    return false;
  }
  const rawPath = url.replace(/^https:\/\/[^/]+/i, '').split(/[?#]/)[0];
  if (parsed.protocol !== 'https:' || parsed.username || parsed.password || (parsed.port && parsed.port !== '443')) return false;
  if (!policy.hosts.includes(parsed.hostname) || parsed.search || parsed.hash || url.includes('?') || url.includes('#')) return false;
  if (rawPath.includes('%') || rawPath.split('/').some((part) => part === '.' || part === '..')) return false;
  return policy.path_prefixes.some((prefix) => parsed.pathname.startsWith(prefix));
}

async function readCapped(response) {
  if (!response.body) return new Uint8Array();
  const reader = response.body.getReader();
  const chunks = [];
  let size = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > MAX_BYTES) {
      await reader.cancel();
      throw new NormalizeError('response_too_large');
    }
    chunks.push(value);
  }
  const bytes = new Uint8Array(size);
  let offset = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return bytes;
}

async function fetchWithinPolicy(url, policy, fetchImpl) {
  const signal = AbortSignal.timeout(FETCH_TIMEOUT_MS);
  let current = url;
  for (let hop = 0; hop <= MAX_REDIRECTS; hop += 1) {
    if (!allowedUrl(current, policy)) return { reason: hop ? 'redirect_outside_policy' : 'url_outside_policy' };
    const response = await fetchImpl(current, { headers: HEADERS, redirect: 'manual', signal });
    if (REDIRECT_STATUSES.has(response.status)) {
      const location = response.headers.get('location');
      await response.body?.cancel();
      if (!location) return { reason: 'redirect_without_location', status: response.status };
      current = new URL(location, current).toString();
      continue;
    }
    if (response.status !== 200) {
      await response.body?.cancel();
      return { reason: `http_${response.status}`, status: response.status };
    }
    return { status: 200, url: current, contentType: response.headers.get('content-type'), bytes: await readCapped(response) };
  }
  return { reason: 'too_many_redirects' };
}

const INTERPRETATION = {
  unchanged: 'The page text matches the verified snapshot. This shows no change since the snapshot; it does not show when the provider last edited the page.',
  updated: 'The page text differs from the verified snapshot, so the page changed after it was verified. Review the current page before relying on curated summaries of it. The change may be unrelated to a specific recommendation, and no publication or update date is known.',
  unavailable: 'The page could not be checked now. Treat curated guidance from this source as dated cached guidance from the snapshot date, not as live-verified.',
  unknown: 'No verified snapshot exists for this source, so a comparison is not possible.',
};

export async function checkFreshness(sourceId, { fetchImpl = fetch, now = () => new Date(), cache, allowFetch = async () => true } = {}) {
  const entry = sourceRecord(sourceId);
  if (!entry) return null;
  const { source, policy, snapshot } = entry;
  const cached = cache ? await cache.get(sourceId) : null;
  if (cached) return { ...cached, live: { ...cached.live, cached: true } };

  const result = {
    source_id: source.id,
    provider: source.provider,
    canonical_url: source.canonical_url,
    status: 'unknown',
    checked_at: now().toISOString().replace(/\.\d{3}Z$/, 'Z'),
    snapshot: { verified_at: snapshot.verified_at, content_sha256: snapshot.content_sha256 },
    live: { http_status: null, content_sha256: null, reason: null, cached: false },
    publication_date: null,
    update_date: null,
    interpretation: '',
  };
  if (!(await allowFetch(sourceId))) {
    result.status = 'unavailable';
    result.live.reason = 'rate_limited';
  } else {
    try {
      const fetched = await fetchWithinPolicy(source.canonical_url, policy, fetchImpl);
      result.live.http_status = fetched.status ?? null;
      if (fetched.reason) {
        result.status = 'unavailable';
        result.live.reason = fetched.reason;
      } else {
        const digest = await sha256Hex(normalize(fetched.bytes, fetched.contentType));
        result.live.content_sha256 = digest;
        if (!snapshot.content_sha256) result.status = 'unknown';
        else result.status = digest === snapshot.content_sha256 ? 'unchanged' : 'updated';
      }
    } catch (error) {
      result.status = 'unavailable';
      result.live.reason = error instanceof NormalizeError ? error.message
        : error?.name === 'TimeoutError' || error?.name === 'AbortError' ? 'timeout' : 'network_error';
    }
  }
  if (!snapshot.content_sha256) result.status = 'unknown';
  result.interpretation = INTERPRETATION[result.status];
  if (cache && result.live.reason !== 'rate_limited') await cache.put(sourceId, result);
  return result;
}
