# Standalone and Skill + MCP regression (0.3.0, `promptingcraft`)

Codex CLI, 2026-10-13, `codex exec --disable apps -s read-only --ephemeral` in a fresh empty
directory per run, one run per case; same operator, so not independent reproduction. Raw
streams stay outside Git. The fallback cases are in `evals/mcp/cases.json`; the other prompts
follow `evals/native/cases.json`.

- **Skill + MCP:** plugin `promptingcraft@dondego-local` 0.3.0 installed and enabled; the
  plugin declares `https://mcp.promptingcraft.com/mcp` (production 8221b270).
- **MCP failure:** as above, with the plugin's server URL overridden to a missing path.
- **Standalone:** plugin uninstalled for these runs (Codex ignores `enabled=false` for a
  plugin's MCP server, so uninstalling was the only clean way); the skill installed with
  `scripts/install_skill.py --host codex` into the run directory.

| Case | Mode | Skill loaded | PromptingCraft.com MCP calls | Observed result |
| --- | --- | --- | --- | --- |
| Explicit `$promptingcraft`, draft / critique / final | Skill + MCP | plugin | search, get, freshness (fixed ids) | Draft and critique shown; found the task already suitable and returned it unchanged; guidance labeled live-verified from the freshness check |
| Natural language, unknown executor model | Skill + MCP | plugin | search, get, freshness | Final prompt kept API shape, no-deploy and no-dependency constraints; said model-specific tuning is unestablished |
| Explicit no-change | Skill + MCP | plugin | search, get, freshness | Exact no-change sentence and original text |
| MCP failure (server unreachable) | Skill + MCP | plugin | none reached the server | Said "PromptingCraft.com's guidance tools were unavailable; official docs were retrieved directly", dated the replacement evidence |
| Explicit, live retrieval unavailable, no-change | Standalone | standalone | none (no server configured) | No-change; "Used bundled Codex references dated 2026-10-12. PromptingCraft.com guidance retrieval and live documentation verification were unavailable." |
| Natural language, draft / critique / final | Standalone | standalone | none | Draft, critique and final; left the empty-date policy open; guidance retrieved from official docs and dated; said the guidance tools were unavailable |
| Immutable manifest, discussion only | Standalone | standalone | none | No-change; manifest preserved exactly; said PromptingCraft.com guidance retrieval was unavailable |
| Negative (explanation request) | Standalone | not loaded | none | Two-sentence explanation, no handoff |

An earlier pass of the same matrix was discarded: the former `promptcraft` plugin was still
installed and was read in some runs, and the "standalone" runs still reached the server
through the plugin. The local `promptcraft` installation was then removed.

Cursor CLI (Auto, reported as Composer 2.5 Fast), skill copied to `~/.cursor/skills/promptingcraft`
by `scripts/evaluate_triggers_cursor.py`, 2 runs each: "Use the promptingcraft skill …"
loaded it 2/2; `/promptingcraft` as non-interactive `-p` text 0/2 and a natural-language
Cursor prompt request 0/2, the same pattern as with the former identifier
(`evals/results/cursor-trigger-1/`). Automatic activation in Cursor remains unestablished.

ChatGPT: in an ordinary ChatGPT conversation with the server added as a custom MCP
connector, `search_guidance` and `get_guidance` were called and returned an official Codex
documentation record with its pinned source (reported by the owner). That shows MCP
availability and invocation in ChatGPT; activation of the bundled skill in ChatGPT has not
been observed.

These runs check behavior and honesty labels; they are not quality benchmarks and do not
change the published 14-case results.
