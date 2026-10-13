# Guidance MCP server: data boundary

What reaches `https://mcp.promptingcraft.com/mcp` besides the tool arguments, and what the
server does with it. Observed on 2026-10-13; the public privacy policy (section 5.3 at
https://promptingcraft.com/privacy) is written from this record.

## Request path

Client (ChatGPT servers, or a local client such as Codex) → HTTPS → Cloudflare edge (adds
network headers) → Worker `promptingcraft-mcp` → body read and size-checked → MCP SDK
transport (stateless, JSON responses) → zod validation of `arguments` only → tool handler.
JSON-RPC `params._meta` and all HTTP headers are received before any validation; the input
schemas do not cover them.

## Method

A temporary build (local branch, never merged; deployed as version `58ef36b5` for about 25
minutes, then rolled back to `8221b270`) printed one line per request to a live
`wrangler tail` session: header **names**, JSON-RPC param keys, argument keys and the key
names and value **types** of `params._meta`. No values were printed or stored; Workers
Logs were off, so the lines existed only in the live stream. Clients: the owner's ChatGPT
account (web, Work mode, custom MCP server) and Codex CLI 0.162.1 with the local 0.3.0
plugin, which declares the server in `mcp.json`.

## Observed

| Client | `tools/call` arguments | `params._meta` (names) | Extra headers (names) |
| --- | --- | --- | --- |
| ChatGPT (web, Work mode) | only schema keys (`target_agent`, `model_family`, `limit`; `id`) | `openai/subject`, `openai/session`, `openai/organization`, `openai/request_id`, `openai/userLocation` (`country`), `callId`, `itemId`, `sessionId`, `windowId`, `progressToken`, `traceparent` | `x-openai-subject`, `x-openai-session`, `traceparent`, `tracestate`, `x-datadog-*`, `user-agent`, `mcp-protocol-version`, `mcp-method` |
| Codex through OpenAI's connector bridge (`codex_apps`, server connected in ChatGPT) | only schema keys (`target_agent`, `model_family`, `scope`, `topic`, `limit`; `id`; `source_id`) | as ChatGPT, with `openai/userLocation` holding `country`, `region`, `city`, `timezone`, `latitude`, `longitude` | as ChatGPT, plus `x-forwarded-for` |
| Codex (plugin `mcp.json`, direct) | only schema keys | `x-codex-turn-metadata` (`model`, `codex_version`, `reasoning_effort`, `sandbox`, `sandbox_mode`, `session_id`, `thread_id`, `turn_id`, `turn_started_at_unix_ms`, `turn_trigger`, `thread_source`, review flags), `plugin_id`, `threadId`, `sessionId`, `callId`, `itemId`, `windowId`, `progressToken` | `user-agent`, `mcp-protocol-version` |
| All | — | — | Added by Cloudflare: `cf-connecting-ip`, `x-real-ip`, `cf-ipcountry`, `cf-ray`, `cf-visitor`, `x-forwarded-proto` |

ChatGPT connects from OpenAI's servers, so its connecting IP is OpenAI's; Codex connects
from the user's machine, so its connecting IP is the user's. When the same account also
had the server connected in ChatGPT, Codex (with its `apps` feature on) reached it a second
way, through OpenAI's connector bridge, from OpenAI's servers. `initialize` carried
`clientInfo` (name and version) from both. ChatGPT also sent `server/discover` with client
capability metadata.

Not observed: conversation text, prompt text, summaries of the conversation, file paths,
code, `openai/locale` or `openai/userAgent`. OpenAI documents more possible fields than we
observed, and hosts can change what they send; absence in these runs is not a guarantee.

## Skill behavior with and without the server (Codex, 2026-10-13)

Same request (a Claude Code prompt for one flaky test, "check the official guidance
first"), empty directory, read-only sandbox:

- Server reachable: the skill was loaded and called `search_guidance` (claude-code,
  context-and-structure), `get_guidance` and `check_source_freshness` twice, with no task
  text in the arguments; it answered no-change and labeled the guidance live-verified.
- Server unreachable (plugin URL pointed at a non-existent path, `apps` disabled): no call
  reached the server; the skill used the official Claude Code documentation through other
  tools, labeled it live-verified and again answered no-change. It did not say that the
  PromptingCraft.com server was unavailable, which `SKILL.md` asks for.

## Handling

- Answers use only the validated arguments; `_meta` and headers are ignored. Tests send
  the observed field names with fake values and check that the answer is identical and
  never contains them (`mcp/test/server.test.js`).
- Nothing is logged: no `console` calls (tested), Workers observability off, script Logpush
  `false`, no tail consumers (Cloudflare API, 2026-10-13). Account-level Logpush jobs could
  not be read with the available token.
- The connecting IP is the key of the per-location Workers Rate Limiting counters.
- The only stored data are freshness results for public pages (Cloudflare cache, 15 minutes;
  60 s for failures), keyed by source id.

Developed by the dondego.com team.
