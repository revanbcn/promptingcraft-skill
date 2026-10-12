Here is the Codex handoff. I didn't run it or touch any code.

```text
Fix the dialog so Escape closes it, following the existing interaction.

Context
- Repository paths are unknown. Find the dialog and its current close behavior (for example, how it closes today and how that is handled) in the codebase.
- If more than one dialog is equally plausible as the target, don't pick one silently. Report the candidates and ask which one is meant.

Authority
- Editing files and running tests are authorized.
- Do not add new dependencies.
- Do not commit.
- Do not deploy.

Verification
- Show observable evidence that pressing Escape closes the dialog and that it closes the way it already does by other means. Run the existing tests that cover it. Report what you ran and the results, including any failures or anything you couldn't run.

Optional suggestion: after the fix, you may suggest an accessibility audit of the dialog. This is only a suggestion. It is not a release gate or a completion requirement.
```

- **Unknowns:** The dialog, the paths and the existing close mechanism are left for the executor to discover. I didn't invent any of them. If several dialogs fit, the prompt asks the executor to check with you rather than guess.
- **Scope:** "Following the existing interaction" is kept as a behavior to match. It doesn't require reusing a specific code path. The no-new-dependencies rule is also kept narrow, so it doesn't freeze manifests or lockfiles.
- **Process:** I added no ban on planning and no extra gates. The only checks are direct evidence for the requested behavior.
- **Source freshness:** I used only the offline `guidance.md` fixture (snapshot 2026-10-10) and the dated Codex notes (checked 2026-10-12). Neither is live-verified official guidance. The executor model isn't established, so nothing in the prompt is tuned to a model.
- **Review:** I did one self-review pass comparing your request with the final text in both directions. That isn't independent verification.