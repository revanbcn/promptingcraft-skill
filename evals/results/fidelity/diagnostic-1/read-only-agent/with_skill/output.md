The prompt is below. I only composed it and did not investigate anything.

```
Investigate why the nightly import duplicates invoices, using the provided redacted log and the repository. This is a read-only investigation.

Return:
1. Likely causes, ranked by how well the evidence supports them.
2. Evidence for each cause, citing specific log lines and file/line locations.
3. Unknowns: what you could not determine from the log and repository, and what would settle each one.
4. A proposed fix.

Constraints:
- Do not edit anything.
- Do not rerun the import.
- Do not access production.
- Do not send messages.
- Do not publish anything.
- You may suggest tests for a later, separately authorized fix, but do not run them now.

Context and limits:
- The log is redacted, so some identifiers may be masked. Where redaction limits a conclusion, say so under unknowns.
- The log's and repository's locations are not given here. Find them in the working environment. If you find more than one plausible log or repository, name the candidates and ask which to use rather than picking one.
- Your tools and model are unspecified. Work with whatever read-only access you have, and report anything you could not inspect.
- Mark each statement as observed in the evidence or inferred. Do not present a hypothesis as a finding.
```

Changes and notes:
- **Kept as you wrote it:** the outcome, the four deliverables and every prohibition. Tests are only suggested, never run.
- **Added:**
  - A ranking of causes by evidence strength.
  - Observed-versus-inferred labeling.
  - A note on how redaction limits conclusions.
  - A note that tool access varies.
  - An instruction to ask if the log or repository location is ambiguous.
- **Left open:** the log and repository paths, the target agent and the model. I added no model-specific tuning.
- **Not added:** a ban on commits or other steps you didn't mention.
- **Freshness:** I did no network retrieval. The only guidance I used was the synthetic `guidance.md` fixture (snapshot 2026-10-10) and the skill's general notes, so none of it is live-verified.
- **Check against your request:** I compared the final text with your request in both directions and found no new requirements, permissions or completion gates. This was a manual check, not a script, and the same model wrote and reviewed the prompt.