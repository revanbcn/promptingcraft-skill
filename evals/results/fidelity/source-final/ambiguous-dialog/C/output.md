Here is the handoff. It tells the executor to ask you which dialog to fix before it edits anything.

```
Fix the dialog so Escape closes it, following its existing interaction.

Context:
- Both billing_dialog.py and profile_dialog.py exist. Which dialog is meant has not been selected, and neither has a reuse mechanism. Leave both choices open.
- "Following its existing interaction" describes the behavior to match, such as how the dialog already closes. It does not mandate a particular code path or shared helper.

Before editing, resolve the target with me. Inspect the code as needed, then ask me which dialog to fix. Make no edits until I answer.

Authorized: editing and testing.

Constraints:
- No new dependencies.
- No commits.
- No deployment.

Verify the result by running a test or check that shows Escape closes the chosen dialog. Report what you ran and what it showed.

Optional suggestion: after the fix, you may suggest an accessibility audit. It is not a completion gate.
```

**Notes**
- **Target:** I kept the target unresolved because the two dialogs are equally plausible. The handoff tells the executor to ask you before editing, as you required. It does not pick one or disclose the choice afterwards.
- **Authority:** I preserved edit and test authority only. I added no extra bans or approval gates beyond your three exclusions. The dependency ban is worded as "no new dependencies" and does not freeze manifest or lockfile files.
- **Reuse:** I left the reuse mechanism open. "Existing interaction" is treated as behavior to match, not as a required code path.
- **Accessibility audit:** It stays an optional suggestion inside the prompt and is not an acceptance gate.
- **Guidance:** The supplied `guidance.md` is dated 2026-10-12 and was verified externally. I did not fetch it myself, and I did not include it in the handoff. It supports the shape of the prompt: outcome, constraints, and a check the executor can run. It does not establish how well the prompt will work in practice.
- **Drift check:** I compared the final text with your request in both directions. Every clause traces to your wording or to a direct decomposition of it. Nothing required was dropped, and no new requirement was added.