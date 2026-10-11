```
Task: read-only investigation of why the nightly import creates duplicate invoices.

Context
- You have a repository and a redacted log of an affected run. The user said both were provided but gave no paths. Locate them in your working directory. If you can't find either, say so and continue with what you have. Don't guess at contents.
- You can't see the prompt author's chat history. Treat anything not stated here as unknown.

Hard constraints (read-only)
- Don't edit, create, move or delete any file in the repository.
- Don't run the import, and don't run tests, builds or scripts that could write data. Reading, searching and inspecting files is fine.
- Don't access production systems or credentials. Don't send messages and don't publish anything.
- If the log has unredacted secrets or personal data, don't repeat them in your output.

Investigate
Trace how the import identifies, deduplicates and writes invoices. Compare that with what the log shows. Candidate areas include the idempotency or unique key, retries or re-delivery, overlapping or concurrent runs, checkpoint or cursor handling, and partial failure followed by re-import. These are starting points only. Follow the evidence, and don't force-fit a cause.

Deliver a report with these sections
1. Likely causes, ranked by confidence. For each, give the reasoning.
2. Evidence: file paths with line numbers, and log excerpts (redacted) by line or timestamp. Mark each item as observed or inferred.
3. Unknowns: what you couldn't determine, and what data or access would settle it.
4. Proposed fix: describe the approach and the files it would touch. Don't apply it.
5. Suggested tests for a later authorized fix. Don't run them now.

Acceptance
- Every claimed cause cites specific evidence, or is labeled a hypothesis.
- You changed nothing and ran nothing that mutates state. State this at the end.
```

Notes:
- Your request is a prompt-authoring task, so I only composed the handoff and didn't investigate anything.
- The log and repository paths weren't given. The prompt tells the executor to locate them and not to invent contents.
- The model and tools are unspecified. The prompt avoids model-specific tuning and relies only on read, search and inspect operations.
- The candidate-cause list is a short set of hints, not requirements. It's marked as non-binding so the executor doesn't anchor on it.
- Source freshness: I used the offline `guidance.md` fixture (snapshot 2026-10-10) as dated cached context only. Nothing was live-verified.