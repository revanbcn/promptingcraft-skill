The handoff is below. I did not inspect the codebase, so it has no file paths, framework or commands. The executor has to find those itself.

```
Task: add a keyboard shortcut to this project's UI, following how the UI already handles shortcuts.

Context: You are starting without the author's chat history. The author had no view of the codebase, so the specifics (which action, which key combination, which framework) are NOT established here.
- Action and key combination: if the requester did not specify them, pick the most natural unbound action and key from the surrounding code and docs. Treat that choice as provisional. Say what you chose and why in your final report.
- Everything below that describes the codebase is something you must discover, not assume.

Goal: the new shortcut triggers the intended action and behaves like the existing shortcuts. Before writing anything, find how existing shortcuts are:
- registered (a central keymap, a hook, or per-component listeners);
- scoped (global versus focused);
- guarded (ignored while typing in inputs or textareas, modifier handling, and any platform differences such as Cmd versus Ctrl);
- surfaced to users (tooltips, menus, help or shortcut lists, docs);
- tested.
Reuse those mechanisms. Do not introduce a new shortcut library or pattern.

Constraints:
- Edit files and tests only.
- Do not install dependencies, change configuration or build tooling, or commit, push, merge, or deploy anything.
- Keep the change minimal and in scope.
- Make no unrelated refactors.
- Do not remap or shadow an existing shortcut. If the chosen key conflicts with one, choose another and report it.
- If existing shortcuts are listed in a help view or in docs, add the new one there too, following the same format.

Acceptance:
- Pressing the shortcut performs the action in the intended scope.
- It is suppressed wherever existing shortcuts are suppressed, such as text inputs.
- Add tests in the project's existing test style covering the trigger and at least one suppression or guard case. Add more only where existing shortcuts have the same coverage.
- Run the project's existing test suite, and lint or typecheck if it is configured. Find the commands in the repo, such as package scripts or a README. Do not invent them.

Final report:
- the files changed;
- the shortcut and action you chose, and whether you chose them or were given them;
- the conventions you followed;
- the exact commands you ran with their results. State plainly any that failed or that you could not run. Do not claim success without that output.
```

**Notes**
- **Unknowns:** the target agent and model, the repo, the action and the key were not given. The prompt labels the action and key as provisional and subordinate to existing conventions. It does not name a specific agent or model, and I applied no agent-specific tuning.
- **Authority:** the prompt grants edits and tests only. It gives no permission to commit, merge or deploy.
- **Sources:** the only guidance I used was `guidance.md`, a synthetic fixture dated 2026-10-10. It is cached test context, not live-verified official guidance, and no network retrieval was possible.
- **Review:** I did one self-review pass against the original request. It is not independent verification.