# Original worked examples

Load only when an example helps compose or review a handoff. These are authored
illustrations, not behavioral evaluation results or claims of improved execution.

## Small bug fix

Before: "Write a Codex task. The Save button shows success even when the API
returns an error. Preserve the API shape. Don't deploy."

Draft: "Fix saving and run tests."

Critique: Lost the visible symptom, API compatibility and deployment boundary.
No check demonstrates that an error stops the false success state.

Final:

```text
Fix Save so an unsuccessful API response is not reported as success. Preserve
the API shape. Locate the existing save path and verify the requested failure
behavior. Do not deploy.

Optional suggestion: use the existing error-display pattern if one is available.
```

## Authorized implementation

Before: "Write a Claude Code handoff: add CSV export to the existing report view;
reuse current columns, no backend change. Edits, tests and an MR are authorized;
merge and deployment aren't."

Draft: "Implement CSV export, then ship it."

Critique: "Ship" invents merge/deploy authority. Missing column and backend constraints.

Final:

```text
Add CSV export to the existing report view using its current columns. Make no
backend changes. Edits, tests and an MR are authorized; merge and deployment are
not. Verify the export represents the chosen columns as valid CSV.

Optional suggestion: consult nearby export patterns; retain existing empty-result
conventions if applicable rather than choosing a new one in this handoff.
```

## Performance with measured acceptance

Before: "Write a Codex task: reduce our existing 10,000-row filter benchmark's
p95 from 900 ms to under 300 ms on the same runner, retaining exact results.
No new dependencies; no deployment."

Draft: "Optimize the filter with caching."

Critique: Prescribed an unchosen mechanism and dropped measurement conditions.

Final:

```text
Reduce p95 latency in the existing 10,000-row filter benchmark to below 300 ms
on the same runner and benchmark protocol used for the 900 ms baseline.
Preserve exact filtering results and add no dependencies. Measure the stated
benchmark under its existing protocol to verify the target and unchanged results.
Do not deploy. The optimization mechanism is not prescribed.
```
