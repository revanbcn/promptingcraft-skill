import { test } from 'node:test';
import assert from 'node:assert/strict';
import { NormalizeError, extractText, normalize, sha256Hex } from '../src/normalize.js';

const words = 'Official guidance text that is long enough to count as documentation content for the check. ';
const bytes = (text) => new TextEncoder().encode(text);

test('html.parser semantics: skipped regions, main preference, entities and stray brackets', () => {
  const html = `<html><head><title>T &amp; T</title><script>var a = "<main>";</script></head>
    <body><nav>Menu</nav><main><h1>Guide&nbsp;&amp;&#39;s</h1><p>1<2 and a &lt; b</p><!-- hidden --><aside>Ad</aside>
    <p class='x'  data-y="a>b">Body</p></main><footer>Foot</footer></body></html>`;
  assert.equal(extractText(html).replace(/\s+/g, ' ').trim(), "Guide &'s 1 < 2 and a < b Body");
  assert.equal(extractText('<p>Only body</p><footer>x</footer>').trim(), 'Only body');
});

test('normalization matches Python whitespace and hashing rules', async () => {
  const text = normalize(bytes(`\ufeff<main>\u00a0 ${words.repeat(2)}\u3000</main>`), 'text/html; charset=utf-8');
  assert.equal(text, words.repeat(2).trim());
  assert.equal(await sha256Hex('abc'), 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad');
  assert.equal(normalize(bytes(`# Title\n\n${words.repeat(2)}`), 'text/markdown'), `# Title ${words.repeat(2).trim()}`);
});

test('unusable responses are rejected with stable reasons', () => {
  const reason = (fn) => { try { fn(); } catch (error) { assert.ok(error instanceof NormalizeError); return error.message; } return null; };
  assert.equal(reason(() => normalize(bytes('short'), 'text/plain')), 'no_usable_content');
  assert.equal(reason(() => normalize(bytes(words.repeat(3)), 'application/json')), 'unsupported_content_type');
  assert.equal(reason(() => normalize(bytes(`Just a moment... ${words.repeat(3)}`), 'text/plain')), 'access_challenge');
  assert.equal(reason(() => normalize(new Uint8Array([0xff, 0xfe, 0x00]), 'text/plain')), 'invalid_encoding');
  assert.equal(reason(() => normalize(bytes(`${words.repeat(3)}\x00`), 'text/plain')), 'binary_response');
  assert.equal(reason(() => normalize(new Uint8Array(1_048_577), 'text/plain')), 'response_too_large');
});
