// Port of normalize() in scripts/freshness.py (Python 3.14 html.parser semantics) so that
// a page fetched here hashes to the same SHA-256 as the verified snapshot in
// sources-baseline.json. Parity is tested against real pages (see mcp/README.md).
import { decodeHTML } from 'entities';

export const MAX_BYTES = 1_048_576;

const SKIP = new Set(['script', 'style', 'nav', 'header', 'footer', 'aside', 'noscript']);
const MAIN = new Set(['main', 'article']);
// html.parser CDATA_CONTENT_ELEMENTS and RCDATA_CONTENT_ELEMENTS (Python 3.14).
const RAW_TEXT = new Set(['script', 'style', 'xmp', 'iframe', 'noembed', 'noframes']);
const RCDATA = new Set(['textarea', 'title']);
const MIME = new Set(['text/html', 'text/plain', 'text/markdown', 'text/x-markdown', 'application/xhtml+xml']);
// Python str.isspace() set, which \s matches in Python's re for str patterns.
const PY_SPACE = '\\t\\n\\v\\f\\r \\x1c-\\x1f\\x85\\xa0\\u1680\\u2000-\\u200a\\u2028\\u2029\\u202f\\u205f\\u3000';
const SPACE_RUN = new RegExp(`[${PY_SPACE}]+`, 'gu');
const EDGE_SPACE = new RegExp(`^[${PY_SPACE}]+|[${PY_SPACE}]+$`, 'gu');
const CHALLENGES = ['verify you are human', 'just a moment', 'access denied', 'checking your browser', 'captcha challenge'];

export class NormalizeError extends Error {}

// Returns the end index of a tag starting at `start` ('<'), honouring quoted attribute values.
function tagEnd(html, start) {
  let quote = null;
  for (let i = start + 1; i < html.length; i += 1) {
    const c = html[i];
    if (quote) {
      if (c === quote) quote = null;
    } else if (c === '"' || c === "'") {
      // Quotes only open inside attribute values (after '='), as in html.parser's attrfind.
      let j = i - 1;
      while (j > start && /[\t\n\r\f ]/.test(html[j])) j -= 1;
      if (html[j] === '=') quote = c;
    } else if (c === '>') {
      return i;
    }
  }
  return -1;
}

export function extractText(html) {
  const parts = [];
  const mainParts = [];
  let skip = 0;
  let main = 0;
  const emit = (data) => {
    if (!data || skip) return;
    parts.push(data);
    if (main) mainParts.push(data);
  };
  const start = (tag) => {
    if (SKIP.has(tag)) skip += 1;
    if (MAIN.has(tag)) main += 1;
  };
  const end = (tag) => {
    if (SKIP.has(tag)) skip = Math.max(0, skip - 1);
    if (MAIN.has(tag)) main = Math.max(0, main - 1);
  };

  let i = 0;
  let text = '';
  const flush = () => {
    if (text) emit(decodeHTML(text));
    text = '';
  };
  while (i < html.length) {
    const lt = html.indexOf('<', i);
    if (lt === -1) {
      text += html.slice(i);
      break;
    }
    text += html.slice(i, lt);
    const next = html[lt + 1] ?? '';
    if (html.startsWith('<!--', lt)) {
      flush();
      const close = html.indexOf('-->', lt + 4);
      i = close === -1 ? html.length : close + 3;
    } else if (next === '!' || next === '?') {
      flush();
      const close = html.indexOf('>', lt + 2);
      i = close === -1 ? html.length : close + 1;
    } else if (next === '/' && /[a-zA-Z]/.test(html[lt + 2] ?? '')) {
      flush();
      const close = html.indexOf('>', lt + 2);
      if (close === -1) { i = html.length; break; }
      const name = html.slice(lt + 2, close).match(/^[^\t\n\r\f />\x00]+/)[0].toLowerCase();
      end(name);
      i = close + 1;
    } else if (next === '/') {
      // '</>' and '</' + non-letter are dropped like html.parser's bogus comments.
      flush();
      const close = html.indexOf('>', lt + 2);
      i = close === -1 ? html.length : close + 1;
    } else if (/[a-zA-Z]/.test(next)) {
      flush();
      const close = tagEnd(html, lt);
      if (close === -1) { text += html.slice(lt); break; }
      const raw = html.slice(lt + 1, close);
      const name = raw.match(/^[^\t\n\r\f />\x00]+/)[0].toLowerCase();
      const selfClosing = raw.endsWith('/');
      start(name);
      i = close + 1;
      if (selfClosing) {
        end(name);
      } else if (RAW_TEXT.has(name) || RCDATA.has(name)) {
        const pattern = new RegExp(`</${name}(?=[\\t\\n\\r\\f />])`, 'i');
        const rest = html.slice(i);
        const found = rest.search(pattern);
        const content = found === -1 ? rest : rest.slice(0, found);
        // Raw text is passed through undecoded; RCDATA has its character references decoded.
        if (content) emit(RAW_TEXT.has(name) ? content : decodeHTML(content));
        i = found === -1 ? html.length : i + found;
      }
    } else {
      // html.parser emits a stray '<' as its own data chunk.
      flush();
      emit('<');
      i = lt + 1;
    }
  }
  flush();
  return (mainParts.length ? mainParts : parts).join(' ');
}

export function normalize(bytes, contentType) {
  if (bytes.byteLength > MAX_BYTES) throw new NormalizeError('response_too_large');
  let text;
  try {
    text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  } catch {
    throw new NormalizeError('invalid_encoding');
  }
  const mime = (contentType || '').split(';')[0].trim().toLowerCase();
  if (!MIME.has(mime)) throw new NormalizeError('unsupported_content_type');
  if (text.includes('\x00')) throw new NormalizeError('binary_response');
  if (mime === 'text/html' || mime === 'application/xhtml+xml') text = extractText(text);
  text = text.replace(SPACE_RUN, ' ').replace(EDGE_SPACE, '');
  if ([...text].length < 100 || text.split(' ').length < 12) throw new NormalizeError('no_usable_content');
  const prefix = [...text].slice(0, 500).join('').toLowerCase();
  if (CHALLENGES.some((phrase) => prefix.includes(phrase))) throw new NormalizeError('access_challenge');
  return text;
}

export async function sha256Hex(text) {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
}
