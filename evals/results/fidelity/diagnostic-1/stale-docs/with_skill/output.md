I composed the handoff below and did not run any of the underlying task.

```text
Fix a small validation bug in this project.

The bug: [PASTE THE VALIDATION PROBLEM HERE: the input, the current behavior, and the expected behavior. These details were not provided to the prompt author. If the code has more than one plausible validation target, ask which one is meant instead of choosing.]

Constraints:
- Preserve the API shape. Do not change the existing request/response structure, field names, types, status codes or public signatures unless the bug description above explicitly requires it.
- Do not deploy.

Context:
- You cannot see the chat that produced this prompt. Find the relevant code yourself.
- Reference guidance available to the prompt author was a cached summary last checked in 2024, with no network access. Treat it as stale, not live-verified or official current guidance. If you rely on Claude Code documentation, check it yourself where you can.

Done when:
- The validation behaves as described in the bug description above.
- You have run an existing test, or a minimal check you can actually run, that shows this behavior, and you report the result.
- You report what you changed and any check you could not run.
```

**Notes**
- **Freshness:** The only guidance was your cached summary from 2024, plus `guidance.md`, a synthetic fixture dated 2026-10-10. Nothing was live-verified. I treated the 2024 summary as stale and did not claim any official source. The handoff says so and keeps model-specific tuning out, since the target model isn't stated.
- **Open item:** You gave no bug details, so the handoff has a placeholder for them. Fill it in before sending. I did not guess a file or rule.
- **Authority:** I kept "preserve API shape" and "do not deploy" as stated. I added no bans on commits or on any other stage, and no planning or test-framework requirements.
- **Drift check:** Every operative clause traces to your request or directly checks the requested fix. The one added item is the instruction to report what changed. The stale-guidance line is context only.
- **Review:** This was a single self-review pass, not an independent check.