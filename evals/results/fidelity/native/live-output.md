The policy descriptions are missing from the supplied conversation. The handoff therefore preserves the comparison request but leaves its substantive input unresolved.

Official guidance was live-verified on **2026-10-12** through Context7 and direct web retrieval. No dedicated official documentation MCP search/read tool was available; web retrieval supplied that fallback. The applicable [Codex prompting guidance](https://learn.chatgpt.com/docs/prompting#prompting-codex) supports clear goals, relevant context, constraints, and verification. No model-specific tuning was applied.

**Source-anchored contract**

| Class | User source | Preserved treatment |
|---|---|---|
| EXPLICIT_REQUIRED | “Discuss the two proposed validation policies using the supplied descriptions; compare tradeoffs and unresolved decisions.” | Discussion and comparison only |
| EXPLICIT_REQUIRED | “Preserve this immutable manifest exactly” | Preserve the literal below verbatim |
| FORBIDDEN | “Implementation has not been authorized”; “Do not execute the underlying task.” | No implementation or task execution |
| FORBIDDEN | “No new dependencies or deployment.” | Preserve both exclusions |
| UNRESOLVED | “The executor model and project paths are unknown.” | No invented model, paths, or environment |
| UNRESOLVED | Policy descriptions absent | Request both descriptions; invent neither |

Immutable literal: `{"version":1,"fields":["job_id","status"],"terminal":"failed_final"}`

**Initial draft**

> Discuss the two proposed validation policies using their supplied descriptions. Compare tradeoffs and unresolved decisions. Preserve exactly: {"version":1,"fields":["job_id","status"],"terminal":"failed_final"}. Implementation is not authorized. Do not execute the task, add dependencies, or deploy. Executor model and project paths are unknown.

**Concise critique**

The draft preserves scope and the manifest, but assumes the descriptions are available. The revision makes that missing input explicit and anchors the comparison to supplied evidence. This was one self-review pass, not independent verification. The final clauses preserve the original constraints without adding implementation mechanisms or completion gates.

**Final copyable prompt**

```text
For Codex: discussion only.

Discuss the two proposed validation policies using the supplied descriptions.
Compare their tradeoffs and identify unresolved decisions. Ground the comparison
in those descriptions, distinguishing stated behavior from assumptions and
missing information. Do not treat discussion as approval to implement or as
selection of either policy.

Missing input: neither policy description was included in this handoff.
Ask: “What are the descriptions of the two proposed validation policies?”
Until they are supplied, explain that the substantive comparison is blocked;
do not invent either policy.

Preserve this immutable manifest exactly:
{"version":1,"fields":["job_id","status"],"terminal":"failed_final"}

Implementation has not been authorized. Do not execute the underlying task.
No new dependencies or deployment.

The executor model and project paths are unknown. Do not assume a specific
model, repository, file path, or shared author environment.
```