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
Fix the settings Save button so an unsuccessful API response shows an error
instead of success. Preserve the existing API shape and follow nearby UI patterns.
Start from the save handler and its callers; their exact paths have not been
provided. Reproduce the failure, make the smallest root-cause fix and run the
affected checks. Verify both a successful save and an API error, including that
the error path never shows success. Do not deploy. Report the changed files,
commands/results and any remaining verification gap.
```

## Authorized implementation

Before: "Write a Claude Code handoff: add CSV export to the existing report view;
reuse current columns, no backend change. Edits, tests and an MR are authorized;
merge and deployment aren't."

Draft: "Implement CSV export, then ship it."

Critique: "Ship" invents merge/deploy authority. Missing column and backend constraints.

Final:

```text
Add CSV export to the existing report view using its current column selection
and ordering. Preserve the backend API and existing report behavior. Inspect
nearby export patterns before choosing the implementation. Verify CSV escaping
for commas, quotes and newlines, empty results and selected-column order; run
the relevant existing checks. Edits, testing and a merge request are authorized.
Prepare the MR with the behavior change and validation evidence; do not merge
or deploy. Report the MR URL and any remaining acceptance limitations.
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
Preserve exact filtering results and add no dependencies. Confirm the baseline
before changing code; locate the bottleneck and choose the smallest appropriate
fix. Compare results for representative edge cases and rerun the benchmark under
the same conditions. Do not deploy. Report baseline/final measurements, protocol,
correctness evidence and any uncertainty that prevents a valid comparison.
```
