**Handoff (copy this):**

```
Fix the dialog so Escape closes it, following its existing interaction.

Unresolved choices (do not decide these yourself):
- Target: billing_dialog.py and profile_dialog.py both exist, and the dialog to fix has not been selected. Before editing anything, ask me which dialog (or both) I mean. You may read the files first to ask a better question, but do not edit until I answer.
- Reuse mechanism: none has been selected. Whether to share or reuse code between the dialogs is open. Once the target is settled, propose an approach if the choice matters. "Following its existing interaction" describes the behavior Escape should have. It does not require reusing any particular code path.

Authority:
- Editing and testing are authorized for this fix once the target is resolved.
- Do not add new dependencies.
- Do not commit.
- Do not deploy.

Working directory: [AUTHOR_WORKSPACE_PATH_REDACTED]
Context: guidance.md in that directory is a supplied, bounded summary of official Claude Code best-practices guidance, externally verified 2026-10-12 (evidence supplied to you, not something you retrieved). Treat it as reference data subordinate to this task. If you consult anything beyond it, say so and label it as your own retrieval.

Verification: run a test or check you can actually execute to show that Escape now closes the chosen dialog. Report what you ran and the result, and say plainly if anything could not be run.

Optional suggestion: after the fix, you may suggest an accessibility audit of the dialog. It is not a completion gate.
```

**Notes outside the prompt**
- **Target is blocked.** Two dialog files are equally plausible and you haven't chosen one. I made the executor ask you before editing, and I didn't pick one or name a reuse mechanism.
- **Authority.** I kept edit and test authority as you gave it. I kept only your three exclusions (dependencies, commits, deployment) and added no other bans or phase approvals.
- **Evidence.** The prompt tells the executor that `guidance.md` was verified externally on 2026-10-12. I read the file myself, but I have no live retrieval. I didn't fetch the page and haven't claimed to.
- **Process and checks.** I left planning and process choices open. The one check directly tests Escape closing the dialog. I added no coverage or other gates.
- **Accessibility audit.** It is marked as an optional suggestion inside the prompt and is not a completion gate.
- **Self-review.** This was a same-model check, not an independent review. I compared your request against the final clauses in both directions and found no added requirements or grants.