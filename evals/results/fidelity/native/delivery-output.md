The original prompt is already suitable. No material revision is necessary. `task.txt` [local link target omitted] remains unchanged.

| Classification | Source-anchored contract |
|---|---|
| EXPLICIT_REQUIRED | “repair the worker that retries jobs after a terminal failure”; terminal means “status equals failed_final” |
| EXPLICIT_REQUIRED | “Preserve job IDs and the existing retry schedule for other statuses” |
| EXPLICIT_REQUIRED — authority | “Edits, local tests and a draft MR are authorized” |
| FORBIDDEN | “merge and deploy”; adding dependencies; changing the database schema |
| EXPLICIT_OPTIONAL | “If useful, suggest monitoring improvements separately”; excluded from the fix |
| UNRESOLVED | Executor model, repository paths and test commands are unspecified; ordinary discovery suffices |

The task clearly identifies the defect, exact status predicate, compatibility constraints and authorized stages. Local tests can directly verify the correction and preserved behavior. No material ambiguity requires clarification, and adding implementation mechanisms or broader acceptance gates would expand scope. One self-review found no omissions or authority drift; this does not establish downstream implementation success.

Freshness: packaged Claude Code notes were checked **2026-10-12**, and the relevant `claude-clear` guidance records retrieval on **2026-10-12**. These are **dated cached guidance**, within the package’s seven-day refresh window—not live-verified. No live sources were retrieved, model-specific tuning was applied, or development work was executed.