Here is the handoff. You didn't say which validation is broken, so I left a placeholder for it instead of making one up.

```
Fix a small validation bug in this project.

Bug: [PLACEHOLDER: describe the validation that is wrong, including the input, the current behavior and the expected behavior. Add the file or endpoint if known.]

Constraints:
- Preserve the API shape. Keep request and response formats, field names, types and status-code contracts unchanged.
- Do not deploy. Local edits and local verification are fine.

Context:
- You can't see the chat that produced this prompt. Find the relevant code yourself and follow the existing patterns.
- The task is small and clear, so go straight to the fix. Planning isn't needed.
- Guidance behind this prompt was a cached summary last checked in 2024. It is dated and was not re-verified. Treat the project's own conventions and docs as authoritative over it.

Done when:
- The bug above is fixed.
- The API shape is unchanged.
- Nothing was deployed.
- Your final report says what changed and shows evidence from a check you actually ran, such as an existing test or a direct reproduction of the bug before and after. If you couldn't run a check, say so.

Optional suggestion: if the project already has a test setup, add a regression test for this case. It is not required.
```

- **Source freshness:** The only guidance was your cached summary from 2024. I treated it as stale and carried that into the prompt as a limitation. The 2026-10-10 `guidance.md` snapshot doesn't make it current. Nothing was verified live, because there's no network.
- **Assumptions:** The executor is Claude Code, and its model is unestablished, so I used no model-specific tuning. I didn't invent file names, commands or a test framework.
- **Drift check:** Your three requirements are covered: a small validation fix, preserve the API shape, and don't deploy. The completion checks only restate those. The regression test is marked optional, and the evidence line is the receipt for the fix itself.