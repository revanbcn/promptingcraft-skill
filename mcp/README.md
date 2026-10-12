# PromptingCraft.com guidance MCP server

Remote MCP server at `https://mcp.promptingcraft.com/mcp` (Streamable HTTP, stateless,
JSON responses, no account or API key). It gives read-only access to the same knowledge
ledger the skill ships, so an assistant can find, cite and freshness-check official
guidance instead of relying on memory.

| Tool | Does | Annotations |
| --- | --- | --- |
| `search_guidance` | Filters curated records by target agent, model family, scope, topic and kind. Inputs are fixed categories; no free text. | read-only, closed world |
| `get_guidance` | Returns one record by stable id: provider, canonical URL, applicability, limitations, labels, verification date, snapshot hash, ledger commit. | read-only, closed world |
| `check_source_freshness` | Fetches one allowlisted registry source and compares its normalized text with the verified snapshot: `unchanged`, `updated`, `unavailable` or `unknown`. Publication and update dates are always `null`. | read-only, open world (fetches public documentation) |

## Source of truth

Nothing here is a second knowledge base. The Worker bundles at build time:

- `skills/promptcraft/references/knowledge.json`: recommendations and PromptingCraft.com methodology;
- `skills/promptcraft/references/sources.json`: the source registry and host/path allowlists;
- `sources-baseline.json`: the verified snapshot (hashes of normalized page text).

`src/catalog-index.json` adds only search facets keyed by ledger ids; a test fails if it
misses or invents a ledger id. Record kinds stay separate: `model_guidance`,
`platform_documentation`, `agent_skills_standard` and `promptcraft_methodology`
(`official: false`, never labelled OFFICIAL). `LEDGER_COMMIT` (set at deploy) pins the
provenance links to the public commit of the ledger.

`src/normalize.js` ports `normalize()` from `scripts/freshness.py` (Python 3.14
`html.parser` semantics). `npm run parity -- <freshness.json>` fetches every registry
source and compares hashes with a Python run; on 2026-10-13 it matched 37/37.

## Privacy and abuse controls

- Inputs are enums and ids validated server-side (unknown keys rejected); no tool accepts
  conversation text, code, paths, URLs or credentials, and errors never echo values.
- Nothing is logged: no `console` calls (tested), Workers observability disabled, no
  Logpush or tail consumers. The only stored data are freshness results for public
  pages, cached in the Cloudflare cache (15 minutes; 60 s for failed checks).
- Rate limits (Workers Rate Limiting binding, per Cloudflare location, best effort and
  eventually consistent): about 600 requests per minute per client IP address (the
  limiter key; hosts share egress addresses), about 6 outbound fetches per minute per source. Request bodies are
  streamed and capped at 64 KiB; JSON-RPC batches are rejected.
- Outbound fetches: registry URLs only, HTTPS, provider host/path allowlist checked on
  every redirect hop (at most 4), one 12 s deadline per check, 1 MiB response cap (the
  Python limit, kept for hash parity), no cookies or credentials. Failed checks are
  cached for 60 s, successful comparisons for 15 minutes.
- Cloudflare processes requests as the hosting provider (see the website privacy policy).

## Develop, test, deploy

```sh
cd mcp && npm ci
npm test                                      # unit and HTTP-surface tests (node:test)
npx -y wrangler@4.149.0 dev --port 8791 --var LEDGER_COMMIT:$(git rev-parse HEAD)
node scripts/inspector-check.mjs http://localhost:8791/mcp /tmp/inspector   # MCP Inspector 2.8.0
```

Deploy only from merged `main` (the ledger commit must be public):

```sh
git switch main && git pull --ff-only && cd mcp && npm ci && npm test
LEDGER=$(git log -1 --format=%H -- ../skills/promptcraft/references/knowledge.json ../skills/promptcraft/references/sources.json ../sources-baseline.json)
npx -y wrangler@4.149.0 deploy --var LEDGER_COMMIT:$LEDGER
node scripts/inspector-check.mjs https://mcp.promptingcraft.com/mcp /tmp/inspector-prod
```

OpenAI domain verification: put the exact token shown in the portal's Connect MCP server
drawer into the Worker secret `OPENAI_APPS_CHALLENGE`
(`npx -y wrangler@4.149.0 secret put OPENAI_APPS_CHALLENGE`); the Worker serves it as
plain text at `/.well-known/openai-apps-challenge`. Rollback:
`npx -y wrangler@4.149.0 rollback <version-id>`.

Developed by the dondego.com team.
