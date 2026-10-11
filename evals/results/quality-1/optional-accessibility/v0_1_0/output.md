```
Task: Make the Escape key close the dialog, matching how the dialog already closes.

Context: The repository paths are unknown, so find the dialog component yourself. Reuse its existing close behavior, such as the close button handler or the overlay-click handler. That covers the state update, callbacks, focus return and any animation. Do not add a separate close path. If the app has several dialogs, start with the one the user most likely means. If more than one fits, pick the one with an existing close interaction, say which you picked, and don't change the others.

Authority: You may edit files and run tests and checks. You may not add dependencies, commit, push, merge or deploy.

Requirements:
- Pressing Escape while the dialog is open closes it the same way the existing close interaction does.
- Escape does nothing when the dialog is closed.
- The key listener is removed when the dialog closes or unmounts.
- Don't change the dialog's other behavior or refactor unrelated code.
- Follow the repository's existing code style and test conventions.

Acceptance:
- Add or update a test that opens the dialog, presses Escape and checks it closed. If the repository has no suitable test setup, say so and describe a manual check instead.
- Run the relevant existing tests and report the exact commands and results. Report failures as they are, including any that were already failing.

Optional: An accessibility audit of the dialog (focus management, ARIA roles) may be worth doing later. Mention it as a suggestion in your final report only. It is not required, and it must not block this change.

Final report: Give the files changed, a short summary of the change, the test results, and any assumptions you made.
```

- **Source freshness:** I used only the synthetic `guidance.md` fixture (dated 2026-10-10). I did not load the Codex-specific notes or any live documentation, so no guidance was verified against official sources.
- **Assumptions:** The prompt tells Codex to pick the dialog itself, since I didn't know the paths. Reusing the existing close handler is how I read "following the existing interaction".
- **Audit:** I kept the accessibility audit as an optional note, so it isn't a release gate.