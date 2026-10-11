Your request didn't name the shortcut's key or the action it triggers, so I left both as placeholders for the executor to fill in. If you can tell me the key and action, I'll put them in. The target agent and model aren't established, so the prompt is agent-neutral. `guidance.md` is a synthetic fixture dated 2026-10-10, and I couldn't retrieve any live sources. The author-side environment says nothing about the executor's, so the prompt names no files or commands.

```
Goal: Add a keyboard shortcut to this project's UI, following the way existing UI behavior already works.

Context:
- The shortcut's key combination and the action it should trigger were not specified in this handoff. [FILL IN: key combination and action.] If they are still blank when you start, find out whether the project documents a convention or an obvious intended action. If neither answers it, stop and ask for the missing choice instead of guessing.
- You cannot see the author's chat history, so inspect the repository yourself to learn how existing shortcuts and UI behavior are implemented.

Requirements:
- Follow existing UI behavior. Match how current shortcuts are registered, scoped, and handled, and how the equivalent mouse or UI action behaves. That includes any existing conventions such as disabled states, focus handling, and conflicts with other shortcuts, where the code already shows them.
- Match the surrounding code's style, naming, and idioms.
- Add or update tests that verify the new shortcut triggers the requested action.

Scope and authority:
- Do edits and tests only. Make code changes and test changes, and run the project's existing tests if your environment allows it.
- Do not commit, push, merge, deploy, publish, or take any other external action.

Report at the end: files changed, tests added or run with their actual results, and anything you could not verify.

Optional suggestion: if the app has user-facing shortcut documentation or a help listing, consider updating it for consistency. This is not required.
```

Checks against your request:
- **Preserved:** adding a shortcut, following existing UI behavior, and edits and tests only.
- **Added as decomposition:** a test that the shortcut triggers its action, which directly verifies the requested result.
- **Kept optional:** the documentation update, which isn't an acceptance gate.
- **Left open:** the key and action.