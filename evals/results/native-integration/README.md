# Native plugin integration evidence — 2026-10-12

## Separate delivery states

| State | Evidence / verdict |
| --- | --- |
| Packaged | Portable Agent Plugins 1.0.0 schema passes; complete skill/resources and two byte-reproducible ZIPs pass; local source materialized without symlinks. |
| Discovered in Codex | `codex plugin list --marketplace dondego-local --available --json` resolves the catalog source from the actual marketplace root. |
| Installed in Codex | `codex plugin add promptcraft@dondego-local`; readback is `installed=true`, `enabled=true`; cache under `plugins/cache/dondego-local/promptcraft/0.1.0`. |
| Native Codex authoring | Five installed-skill activations; six scenarios, seven actual CLI turns, all exit 0. Resources loaded from plugin cache, not a development skill injection. |
| Installed in ChatGPT Desktop | NOT VERIFIED. App exists; supported Computer Use access is denied by app policy. |
| Activated in ordinary Chat | NOT RUN. CLI/Work execution cannot substitute for this state. |
| ChatGPT end to end | NOT RUN. [Exact owner steps](../../../docs/chatgpt-installation.md) prepared. |

The candidate was first registered from an isolated worktree. Delivery will move
only this new local registration to the stable owner checkout after merge and
confirm it. Live delivery readback will be recorded in
[MR !4](https://gitlab.com/revanalex/promptcraft-skill/-/merge_requests/4).
Six prior marketplace records and 52 prior installed-plugin records
remain unchanged in candidate readback; no global configuration file was replaced.

## What actually ran

Codex CLI **0.162.1**, default observed **gpt-6.1-sol** from persisted native
`turn_context`, existing account/config and read-only execution sandbox. Every
session uses an empty authoring directory with no standalone project skill. The
first two turns use **the same persisted thread**, resumed by explicit ID through
`codex exec ... resume`; the conversation is not a pasted multi-turn simulation.
The remaining scenarios start new native threads. Authoring requests do not
execute the proposed development tasks.

Canonical and installed skill digest:
`351b078a9c49e7a650a184a4504ccd2765a901217584d191e1787ebb2f812e40`.
The entire canonical skill is byte-identical to MR !3 (`dbdf3cd`); prior evaluation
cases, assertions and expected contracts are unchanged.

| Scenario | Observed behavior |
| --- | --- |
| [Multi-turn implicit](multi-turn-implicit-turn-2.md) | Context-only turn acknowledges decisions without loading PromptCraft. “Prepare a Codex prompt for this task” loads the installed skill and preserves previously agreed CSV columns/order, action, dependencies, auth and deployment boundary. |
| [Explicit live](explicit-live-turn-1.md) | `$promptcraft` loads resources; requested initial draft and concise critique appear as prose; complete original task body in one final block. No-change is permitted despite the explicit invocation. |
| [No-change / unavailable guidance](no-change-offline-turn-1.md) | No-change statement plus task body echoed exactly; dated/unavailable guidance identified; no documentation retrieval call. |
| [Unresolved identity / capabilities](unresolved-capabilities-turn-1.md) | Both repositories remain open; deciding question comes before repository-specific work. Investigation-only/read-only/no-browser boundaries survive; author retrieval is not executor freshness. |
| [Exploratory immutable manifest](exploratory-manifest-turn-1.md) | Original discussion body and immutable manifest preserved exactly; retry remains a suggestion, planning allowed, implementation unapproved. |
| [Negative activation](negative-activation-turn-1.md) | Two-sentence explanation; no PromptCraft resource read, no execution prompt. |

All five positive responses have one handoff block. Three use no-change; the
no-change CSV body and exploratory manifest have exact-text checks. Readable
contract/rubric/target notes are observed in all five positive traces. The trace
records live OpenAI documentation reads in three scenarios and Claude docs MCP
search/read in the target-Claude scenario. Claude MCP corpus freshness was not
independently HTTP-revalidated; its retrieval date does not prove publication or
executor freshness. The offline scenario deliberately specifies unavailable
retrieval; it is **not** an injected network outage. No authoring task writes are
observed; native CLI session persistence itself writes host session metadata.
[Fresh-context review](review.md) independently compared the actual final clauses
with the original contracts and found 0/5 positive outputs with material drift.
Mechanics and the assistant's own claim do not supply that semantic verdict.

## Cost and limits

[Metrics](metrics.json) record actual responses, resources, retrieval calls,
per-turn tokens/timings and hashed thread identity. Raw native events and ambient
private host data stay outside tracked artifacts. Seven turns took **617.85s**
serially; reported usage sums **1,472,244 input tokens**, including **1,151,104
cached input tokens**, and **12,050 output tokens**. These totals include repeated
contexts and ambient user plugins/tools; they are not unique prompt length, an
incremental PromptCraft cost, or a billed-dollar estimate. Billing cost is not
observed. Some unrelated configured MCP connections had startup errors; useful
documentation reads still completed, and no credentials/settings were repaired.

This is a small set of sanitized synthetic discussions executed by genuine Codex,
not real ChatGPT runs or downstream task executions. No A/B/C superiority or
production usefulness is established. The previous 0/14 semantic sample and
matched downstream findings remain historical evidence from MR !3; they were not
rerun or improved by relabeling this installation test. Recommendation remains
**IMPROVE FURTHER** until native ordinary-Chat usability and successful downstream
outcomes are independently observed. No new release, public-directory submission,
workspace publication, new MCP service or deployment occurs.

Developed by the dondego.com team.
