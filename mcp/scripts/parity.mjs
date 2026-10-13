#!/usr/bin/env node
// Normalization parity check: fetch every registry source once and compare the SHA-256
// of this port's normalized text with the Python reference hashes.
// Usage: node scripts/parity.mjs [python-freshness.json]
// Without an argument it compares with sources-baseline.json (the verified snapshot),
// where a mismatch can also mean the page really changed since that snapshot.
import { readFileSync } from 'node:fs';
import { normalize, sha256Hex, NormalizeError } from '../src/normalize.js';

const root = new URL('../../', import.meta.url);
const registry = JSON.parse(readFileSync(new URL('skills/promptingcraft/references/sources.json', root), 'utf8'));
const reference = process.argv[2]
  ? Object.fromEntries(JSON.parse(readFileSync(process.argv[2], 'utf8')).sources.map((s) => [s.id, s.hash]))
  : Object.fromEntries(Object.entries(JSON.parse(readFileSync(new URL('sources-baseline.json', root), 'utf8')).sources).map(([id, s]) => [id, s.hash]));

const headers = {
  'User-Agent': 'PromptingCraft.com-docs-check/0.2 (public read-only)',
  Accept: 'text/markdown,text/plain,text/html',
  'Accept-Encoding': 'identity',
};
let same = 0;
const differ = [];
for (const source of registry.sources) {
  try {
    const res = await fetch(source.canonical_url, { headers, redirect: 'follow', signal: AbortSignal.timeout(15000) });
    const bytes = new Uint8Array(await res.arrayBuffer());
    if (res.status !== 200) { differ.push(`${source.id}: HTTP ${res.status}`); continue; }
    const hash = await sha256Hex(normalize(bytes, res.headers.get('content-type')));
    if (hash === reference[source.id]) same += 1;
    else differ.push(`${source.id}: ${hash.slice(0, 12)} != ${String(reference[source.id]).slice(0, 12)} (${res.headers.get('content-type')})`);
  } catch (error) {
    differ.push(`${source.id}: ${error instanceof NormalizeError ? error.message : error.name}`);
  }
}
console.log(`parity ${same}/${registry.sources.length}`);
for (const line of differ) console.log(`  differs ${line}`);
process.exit(differ.length ? 1 : 0);
