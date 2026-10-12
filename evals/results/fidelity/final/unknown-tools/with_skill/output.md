The request is for a handoff, so I've composed one and haven't touched any code. The target agent and model aren't established, so the prompt is agent-neutral and has no model-specific tuning. I used `guidance.md` (a synthetic fixture dated 2026-10-10, offline, not live-verified) only as dated general guidance. The executor never sees that file. Your wording survives as written, and I added only context discovery and checks that follow from it.

```
Add a keyboard shortcut following existing UI behavior; edits and tests only.

Context:
- You are starting without the prompt author's chat history. Discover the relevant UI code, any existing keyboard-shortcut handling, and the test setup in the repository yourself.
- Which action the shortcut triggers and which key combination it uses were not specified. If the repository, issue text or surrounding instructions identify them unambiguously, use those. If several actions or key combinations are equally plausible, stop and ask for the deciding choice rather than picking one.

Requirements:
- The new shortcut behaves consistently with how existing UI behavior already works (for example, how existing shortcuts are registered, how they interact with focused inputs, and how the UI reflects them).
- Your actions are limited to editing files and running or writing tests. Do not take other actions, such as deploying or publishing.

Verification:
- Add or update tests that exercise the new shortcut's behavior, and run the relevant tests.
- Report which tests you ran and their results. If you could not run them, say so plainly.

Optional suggestion: if existing shortcuts are listed in a help overlay, tooltip or docs, check whether the new one belongs there too. Treat this as a suggestion, not a requirement.
```

**Notes**
- **Open choice:** you didn't say what the shortcut does or which keys it uses. The prompt leaves that open and tells the executor to ask if the repo gives several equally plausible answers. If you already know them, tell me and I'll put them in.
- **Authority:** "edits and tests only" is kept as the limit on what the executor may do. I added no bans on commits or other steps, and no planning rules.
- **Executor tools:** I made no claims about the executor's tools. The missing terminal and MCP access applies to me as author, not to it.
- **Optional suggestion:** the help-overlay line is labeled optional and isn't a completion check.