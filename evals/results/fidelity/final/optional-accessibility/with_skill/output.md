Here is the handoff, ready to copy. I only composed it and didn't touch any code. Repository paths are unknown, so the executor has to find the dialog itself. I added one clause saying to ask which dialog if several fit equally, because you didn't name one. The executor is Codex. `guidance.md` is a dated fixture from 2026-10-10 and nothing was checked live, so I left it out of the handoff.

```text
Fix the dialog so Escape closes it, following the existing interaction.

Context:
- Repository paths are not known; locate the dialog component and its existing close behavior in the codebase. If more than one dialog is an equally plausible target, ask which one rather than picking one.
- "Following the existing interaction" describes the behavior to match: Escape should close the dialog the way the dialog's existing close actions already do. It does not require reusing any particular code path.

Authority and constraints:
- You may edit files and run tests.
- Do not add new dependencies.
- Do not commit.
- Do not deploy.

Verify: run the relevant existing tests, and add or update a test where the codebase's conventions make that natural. Show evidence that pressing Escape while the dialog is open closes it.

Optional suggestion: after the fix, you may suggest an accessibility audit of the dialog. This is only a suggestion. It is not a release gate or a completion requirement.
```

- **Verify line:** it only checks the behavior you asked for. It doesn't require a new test framework or any coverage threshold.
- **Dependency and commit limits:** "No new dependencies" forbids adding dependencies, but the executor can still touch manifests if needed. Commits and deployment are excluded as you specified.
- **Accessibility audit:** it sits inside the prompt as an optional suggestion, not a requirement.