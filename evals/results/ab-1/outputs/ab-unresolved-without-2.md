```text
Investigate why the billing export drops rows. Investigation only; no edits or fixes.

Repository selection is unresolved: api-east and api-west are equally plausible. Your first response must ask: “Which repository should I investigate: api-east or api-west, and what is its checkout path?” Then wait for the answer. Do not inspect either repository, choose based on the current directory, or combine evidence from both.

After I select the repository:

1. Confirm the checkout path, branch, and commit. Read applicable repository instructions and preserve all existing work.
2. Use read-only inspection. Do not modify files, install dependencies, create artifacts, commit, deploy, trigger export jobs, or change database or external state. Run existing checks only when their lack of side effects is established.
3. Establish the expected export population and observed omissions from available evidence. If necessary, request a sanitized failing example with export parameters, expected rows, and actual output.
4. Trace the export from source query through pagination, filtering, transformation, serialization, and delivery. Find the earliest stage where an expected row disappears.
5. Examine relevant mechanisms such as joins, date/timezone boundaries, pagination termination, deduplication, null handling, swallowed errors, concurrency, and output truncation. Treat these as hypotheses until supported.
6. Compare a missing row with a retained row and, where available, a working sibling code path. Distinguish intentional exclusions from defects.

Return:
- Repository and revision investigated.
- Findings with file:line references and observed evidence.
- Confirmed cause, or ranked hypotheses with supporting and contradictory evidence.
- Remaining unknowns and the smallest read-only check needed to resolve them.

If the cause is unproven, say so. Stop after the investigation report; implementation requires a separate instruction.
```