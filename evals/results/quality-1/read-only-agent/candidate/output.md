The prompt is below. I didn't run anything, and I didn't look at the log or the repository.

```text
Investigate why the nightly import duplicates invoices. Use the provided redacted log and the provided repository. This task is read-only.

Return:
1. Likely causes of the duplicate invoices.
2. Evidence for each cause, such as log lines and file/function references.
3. Unknowns: what you could not determine from the log and repository, and what would settle it.
4. A proposed fix.

Constraints:
- Do not edit any files.
- Do not rerun the import.
- Do not access production.
- Do not send messages.
- Do not publish anything.
- You may suggest tests for a later, separately authorized fix, but do not run them now.

Context:
- The log is redacted. Treat redacted values as unavailable and don't guess them.
- You have no chat history. If the log or repository location isn't given to you, say so in your answer instead of guessing paths.
- Keep what you observed in the log and code separate from what you infer. If the evidence doesn't support a cause, list it under unknowns.

Optional suggestion: order the causes from most to least supported by the evidence.
```

- **Contract:** The prompt keeps your goal, the four requested outputs, the five prohibitions and the "suggest tests, don't run them" rule. It adds no mandatory steps, thresholds or completion gates.
- **Paths:** You said the log and repo are "provided" but gave no paths, so I didn't invent any. The prompt tells the executor to report missing locations instead of guessing them.
- **Added context:** Treating redacted values as unavailable and separating observation from inference is context I added. It doesn't change what you asked for. The ordering by evidence strength is marked optional.
- **Tools and model:** Both are unspecified, so the prompt is general. I did no model-specific tuning.
- **Sources:** The only guidance was the synthetic fixture dated 2026-10-10. It isn't live-verified, and I did no network retrieval. I compared the final clauses against your request by hand. I didn't run the optional checker.