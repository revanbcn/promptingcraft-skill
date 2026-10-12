```text
Investigate why the billing export drops rows. This is investigation only; no edits.

The target repository is unresolved: api-east and api-west are equally plausible, and neither has been selected. First ask me which repository to investigate, or whether to compare both. Do not silently choose a repository or begin repository-specific diagnosis before I answer.

Constraints:
- Do not modify files, configuration, data, dependencies, or Git state.
- Do not create plans, reports, temporary files, or other artifacts on disk.
- Use read-only inspection. Avoid running exports, tests, or other commands that write files or mutate external systems.
- Do not expose credentials or sensitive billing records.

After the repository scope is confirmed:

1. Establish the export entry point, output format, relevant version/environment, expected row count, and observed row count. Request missing evidence when it prevents a reliable diagnosis.

2. Trace rows from source selection through the final exported output. Inspect filters, joins, pagination, batching, deduplication, date/time boundaries, validation, serialization, and error handling. Distinguish intended exclusions from unintended losses.

3. Where evidence permits, trace a missing row and a comparable included row through the same path. Identify the first stage where the missing row disappears and the exact predicate or failure responsible. Use sanitized identifiers.

4. Check existing tests and available logs for evidence supporting or contradicting each hypothesis. Do not infer the cause from an error name or a suspicious code fragment alone.

5. If both repositories are authorized, keep findings separate and establish which implementation handles the affected export before attributing the defect.

Return an inline report containing:
- Repository and version investigated.
- Confirmed findings, with file:line references and available count/log evidence.
- The first proven row-loss stage and mechanism, if established.
- Remaining hypotheses, missing evidence, and the smallest next read-only diagnostic step.

Do not implement a fix. If the cause cannot be established, state that clearly.
```