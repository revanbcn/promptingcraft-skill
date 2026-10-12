Here is the handoff. The target is Codex, and the model is unestablished.

```
Fix the dialog so Escape closes it, following the existing interaction.

Context:
- The repository paths are unknown. Locate the dialog component and any existing close behavior (for example the close button or backdrop click) in the codebase. If more than one dialog is plausible, say which one you chose and why.
- "Following the existing interaction" means Escape should behave as the dialog's existing close interaction does. Reuse of any particular code path is not required.

Authority:
- You may edit files and run tests.
- Do not add new dependencies.
- Do not commit.
- Do not deploy.

Verify: show observable evidence that pressing Escape closes the dialog (a test, or a reproduction you ran). Report the commands you ran and their results. If something could not be run or verified, say so.

Optional suggestion: you may recommend an accessibility audit of the dialog as a follow-up. This is not a release gate and not part of completion.
```

Notes:
- **Scope:** the prompt keeps your wording and adds only discovery context and a direct check of the Escape behavior. It does not name files, a mechanism, or extra test requirements.
- **Open choice:** if several dialogs fit, you didn't say which one. I asked the executor to state its pick rather than silently choosing. If you know which dialog you mean, name it in the prompt.
- **Authority:** edit and test are granted as you stated. Commits and deployment are excluded as you stated. I added no other bans or grants. Dependency manifests are not frozen, only the addition of new dependencies is forbidden.
- **Freshness:** Codex guidance came from the skill's dated offline notes, checked 2026-10-12. I did no live retrieval. I did not pass `guidance.md` to the executor.
- **Review:** this was a same-model self-review, not independent verification.