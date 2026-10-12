The original prompt is already suitable. No material revision is necessary.

```
Investigate why the nightly import duplicates invoices using the provided redacted log and repository. This is read-only. Return likely causes, evidence, unknowns and a proposed fix. Do not edit, rerun the import, access production, send messages or publish. You may suggest tests for a later authorized fix, but do not run them now.
```

**Checks on the original**
- **Goal and mode:** The goal is to investigate, and the mode is read-only. The four requested outputs are likely causes, evidence, unknowns and a proposed fix. These are preserved as written.
- **Authority:** The prompt grants no edits, no import rerun, no production access, no messages and no publishing. It allows only suggesting tests, not running them. Nothing needs adding, and a generic "ask before acting" clause would only add process.
- **Acceptance:** The four deliverables are a feasible check. Evidence and unknowns are separate, so the executor can't pass off guesses as findings.
- **Model and agent:** The target model and tools are unspecified, so I applied no model-specific tuning. The prompt is plain enough for any agent that can read files.

**Limitations**
- **Input paths:** "The provided log and repository" depends on the executor receiving those inputs. If it finds more than one plausible log or repository, it should ask which to use rather than pick one. I left that out of the prompt because it is ordinary discovery, and the user's words don't call for it.
- **Guidance freshness:** I used `guidance.md` (a synthetic fixture dated 2026-10-10) and the skill's offline notes only. No live official sources were retrieved, and the guidance is not live-verified.
- **Review:** This was a single self-review pass, with no independent reviewer and no downstream test of the prompt.