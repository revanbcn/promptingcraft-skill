The handoff is below. The request doesn't say which action or key combination the shortcut should use, so I left both as placeholders. Please fill them in, or tell me and I'll finalize it.

```text
Add a keyboard shortcut following existing UI behavior.

Shortcut to add:
- Action: [UNRESOLVED – not yet specified]
- Key combination: [UNRESOLVED – not yet specified]
If either is still unfilled when you read this, stop and ask for it before editing. Do not choose one yourself.

Scope: edits and tests only.

Context:
- You have no chat history. The repository layout, framework and existing shortcut handling are unknown to the author, so discover them in the codebase.
- "Following existing UI behavior" means the new shortcut should behave like the shortcuts and the equivalent UI action already in the app. Check how those are triggered, enabled and disabled, and how they behave when focus is in a text field. You are not required to reuse any particular code path.

Verification:
- Add or update tests showing that the new shortcut triggers the requested action and matches the existing UI behavior.
- Run the project's existing tests and report the results, including any failures.

Optional suggestion: if the app lists shortcuts in a help screen, tooltip or docs, consider listing the new one there too. This is not required.
```

Notes:
- **Authority:** "Edits and tests only" is carried over as the scope. I didn't add bans on other actions, and I didn't grant any commit, push or deploy.
- **Target and model:** No target agent or model was given, so the prompt is agent-neutral and has no model-specific tuning. The author's `guidance.md` is a dated synthetic fixture (2026-10-10). It isn't live-verified, and I didn't put it in the handoff.
- **Deciding question:** Which action should the shortcut trigger, and with which keys?