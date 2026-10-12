The prompt is below. You didn't say which validation bug to fix or where it lives, so I left a placeholder for it and made no guesses.

```
Fix a small validation bug in this project.

Bug to fix: [PLACEHOLDER: describe the validation behavior that is wrong, what it does now, and what it should do. Add the file or endpoint if known.]

Constraints:
- Preserve the API shape. Do not change request or response structures, field names, status codes, or endpoint signatures beyond what the validation fix itself requires. If the fix seems to need such a change, stop and report it instead of making it.
- Do not deploy. Do not merge, publish, or trigger any release or deployment workflow.

Context:
- You can't see the conversation this prompt came from. Read the relevant code and any existing tests first, and follow the existing patterns.
- This is a small, clear fix. Proceed directly without a separate planning phase.
- The author's only guidance reference was a cached summary last checked in 2024. It was not verified live and may be out of date. If a tool or workflow detail matters to your approach, check it against what is actually installed or documented in your environment.

Verification:
- Run the project's existing tests or an equivalent check you can actually run. Add or adjust a focused test only if that is the simplest way to show the bug is fixed. Report the result honestly, including any failures or checks you couldn't run.
- Confirm that the request and response shape is unchanged.

When finished, report the files changed, what the fix does, and the verification evidence.
```

- **Placeholder:** the bug description is the only missing input. Fill it in before use.
- **Source freshness:** the 2024 cached summary is carried into the handoff as unverified. `guidance.md` is a synthetic fixture dated 2026-10-10, not official guidance, so I did not treat it as updating that summary. No network retrieval was possible.
- **Target model:** the executor's model is unknown, so I used Claude Code general guidance only. Examples are outcome, context, constraints, and a runnable check.
- **Contract check:** I compared the final prompt against your request by hand. The only operative clauses are "preserve API shape" and "do not deploy", both from your words, and the verification steps test those directly. I added no other requirements.