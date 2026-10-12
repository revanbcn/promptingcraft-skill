The request doesn't say which action gets the shortcut, which key it uses, or which UI it belongs to. I left those as fields for you to fill in. The executor can't discover them from the repo, so please fill them in before sending.

```
Goal: Add a keyboard shortcut following existing UI behavior.

Fill in before sending (the executor cannot infer these):
- Action the shortcut triggers: [UNSPECIFIED]
- Key or key combination: [UNSPECIFIED]
- Screen or component it applies to: [UNSPECIFIED]
If any of these is still unspecified when you start, stop and ask one focused question. Do not choose one yourself.

Context:
- You have no access to the author's chat history, and the repository layout is unknown to the author. Discover the relevant files yourself.
- "Following existing UI behavior" means the shortcut should behave like the app's existing shortcuts and the existing click or menu path for the same action. Examples are focus handling, disabled states, and whether it works while typing in an input. Match how the codebase already does this. Reusing a particular mechanism is not required.

Authority: edits and tests only. Do not take any other action, such as deploying or publishing.

Done when:
- The shortcut triggers the specified action, consistent with the existing UI behavior above.
- Tests covering the new shortcut exist and pass. Use the project's existing test setup.
- Report what you changed, which tests you ran, and their results. If you couldn't run something, say so.
```

Notes:
- **Sources:** I used the dated synthetic `guidance.md` (snapshot 2026-10-10) as offline context only. It is not live-verified, and no network retrieval was available.
- **Target agent:** The target agent and model weren't selected, so I wrote it as general guidance. No agent-specific or model-specific tuning is applied.
- **Drift check:** I compared the final clauses against your request and found nothing added. The only operative requirements are the shortcut, following existing UI behavior, edits and tests only, and passing tests. The report line only asks the executor to say what it did.

**Deciding question:** What action, key, and screen should the shortcut cover?