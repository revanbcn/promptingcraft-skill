Here is the handoff. The target dialog and any reuse mechanism are unresolved, so the prompt makes the executor settle the target with you before it edits. I didn't read or touch the code.

```
Fix the dialog so Escape closes it, following its existing interaction.

Context:
- billing_dialog.py and profile_dialog.py both exist. Which dialog this task means has not been selected, and neither has a reuse mechanism. Both are open choices.
- Your working directory is the project root. Locate these files and any related code yourself.

Target resolution (do this first):
- Resolve the target dialog with the user before editing anything. You may read code to find out what each dialog does and how it handles Escape and closing. Then ask the user which dialog is meant, and wait for their answer.
- Do not pick a dialog yourself. If you find a reuse mechanism that might apply, offer it as an option for the user to decide, not as a requirement.

Once the target is confirmed:
- Edit and test are authorized.
- Make Escape close the selected dialog, matching how that dialog already opens, closes and handles input. Matching the existing interaction is about behavior. It does not require reusing any particular code path.
- Run relevant tests or another check you can actually run, to confirm that Escape closes the dialog. Report what you ran and what it showed. If you could not run a check, say so.

Constraints:
- No new dependencies.
- No commits.
- No deployment.

Optional suggestion: when you finish, you may suggest an accessibility audit of the dialog. This is not a completion gate.
```

**Notes**
- **Preserved from your request:**
  - The goal, and following the existing interaction.
  - Edit and test authority.
  - Resolving the target with you before editing.
  - No new dependencies, commits or deployment.
  - The accessibility audit as an optional suggestion, not a gate.
- **Left open:** which dialog, and any reuse mechanism. The executor asks you about the dialog, so it can't choose one and tell you afterward.
- **Not added:** planning rules, extra test requirements or mandated mechanisms.
- **Evidence:** the supplied `guidance.md` is verified, dated 2026-10-12, and its publication date is unknown. I didn't retrieve anything live. Nothing here shows how well the handoff will work downstream. I checked the draft against your wording once, myself, with no separate reviewer.