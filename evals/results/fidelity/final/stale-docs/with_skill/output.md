Here is the handoff. The task text you gave doesn't say which validation is broken, so I left a placeholder for that.

```
Make a small fix to a validation bug in this project.

Bug (fill in before sending: the input, the current behavior, and the expected behavior):
[DESCRIBE THE VALIDATION FAILURE HERE]

Constraints:
- Preserve API shape.
- Do not deploy.

Context:
- You don't have the prompt author's chat history. Locate the relevant validation code yourself.
- If the bug description above matches more than one plausible place in the code, ask which one is meant before editing.

Verification:
- Reproduce the reported failure first, then show that the fix resolves it, using a test or command you can actually run in this repo.
- In your final report, give the evidence you ran and say if anything couldn't be verified.

Optional suggestion: if a test for this validation already exists, extend it instead of adding a new one.
```

- **Kept from your request:** the small validation fix, "Preserve API shape" and "do not deploy". The API-shape constraint has no exceptions.
- **Added:** only discovery and verification wording. It also says to ask if the bug could match more than one place. I didn't add bans on commits or merges, because you didn't ask for them.
- **Missing:** the bug details. I didn't invent any. The executor needs them to reproduce the failure, so fill in the placeholder.
- **Executor:** Claude Code is assumed from your request. No model is named, so I used no model-specific tuning.
- **Guidance freshness:** I had no network access. The Claude Code guidance I used is a dated cached note (checked 2026-10-12). It is not live-verified. Your 2024 cached summary is older than that, so treat it as stale. `guidance.md` is only my reference context and I didn't put it in the handoff.
- **Review:** I checked the handoff against your original request once, and it adds no new requirements or permissions. That was a self-review, not an independent one, and it says nothing about whether the fix will work.