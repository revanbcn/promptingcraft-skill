The handoff is below. It tells the executor to ask you which dialog to fix before it edits anything. It treats the reuse mechanism as an open choice.

```
Task: Fix the dialog so Escape closes it, following its existing interaction.

Context:
- Both billing_dialog.py and profile_dialog.py exist. Which dialog is meant has not been decided, and neither has any reuse mechanism (for example a shared helper). Both are open choices.
- "Following its existing interaction" describes the behavior to match: Escape should close the dialog the way the dialog already closes. It does not require reusing any particular code path.
- You have no access to the chat that produced this task. Find paths and the test setup by looking at the project.

Before editing:
- Resolve the target with the user first. Ask which dialog (billing_dialog.py, profile_dialog.py, or both) should get the fix, and wait for the answer. Do not pick one yourself.
- You may read code and look around while you wait. Make no edits until the target is settled.

Authority:
- Once the target is resolved, you may edit and run tests.
- Do not add new dependencies.
- Do not commit.
- Do not deploy.

Done when:
- Pressing Escape closes the chosen dialog, and the way it closes matches how that dialog already closes.
- Report what you changed and the test or check evidence you actually ran. If you could not run something, say so.

Optional suggestion: Afterward, you may mention that an accessibility audit of the dialog(s) could be worthwhile. This is not part of completion.
```

- **Target:** The task didn't choose between the two files, so the handoff makes the executor ask you and wait. It can still read code in the meantime.
- **Reuse:** "Existing interaction" is written as a behavior to match, not as a mechanism to reuse.
- **Authority:** Edit and test are granted only after the target is resolved. The ban on new dependencies, commits and deployment is carried over as you gave it. It does not freeze manifests or lockfiles.
- **Accessibility audit:** It appears only as an optional suggestion and is not a completion gate.
- **Model and guidance:** The executor is Claude Code, and the model is unknown. Guidance came from `guidance.md` (a synthetic fixture dated 2026-10-10) and the skill's cached Claude Code notes. Nothing was retrieved live, so none of it is current official guidance.