```
Fix the dialog so that pressing Escape closes it. Follow the dialog's existing interaction: close it the same way its other close actions do, and reuse that existing path and its conventions instead of introducing a new one.

Context:
- I don't know the repository layout or file paths. Find the dialog component and its existing close behavior yourself. If more than one dialog could match, pick the one that fits the request. If it's still ambiguous, say which you chose and why.
- You may edit files and run tests for this task.

Constraints:
- Do not add new dependencies.
- Do not commit.
- Do not deploy.

Done when:
- With the dialog open, pressing Escape closes it, and it closes the same way the existing close actions do.
- Existing close behavior still works.
- You ran the relevant existing tests, or added a test for Escape if that fits the repo's conventions, and report the actual results. If you couldn't run tests, say so and why.

In your final report, list the files you changed, summarize the change, and give the test output.

Optional suggestion: if it's convenient, mention whether an accessibility audit of this dialog would be worthwhile. This is not required and is not a completion criterion. Don't run or block on one.
```

Notes:
- **Scope:** I kept it to your words: Escape closes the dialog, follow the existing interaction, edit and test allowed, and no new dependencies, commits or deployment.
- **"Existing interaction":** I read this as reusing the dialog's current close path. I didn't add requirements such as focus return or backdrop behavior, since you didn't ask for them.
- **Paths:** Because they're unknown, the executor has to find the dialog itself.
- **Accessibility audit:** It's an optional suggestion inside the prompt, not a gate.
- **Sources:** The only guidance was the dated synthetic `guidance.md` (snapshot 2026-10-10) and the offline Codex notes. There was no live retrieval, and I haven't assumed which model the executor is.