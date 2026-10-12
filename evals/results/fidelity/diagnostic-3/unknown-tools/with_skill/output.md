Your request didn't say which shortcut or which action it triggers, so the handoff leaves both as fill-in fields. I didn't guess them. If you give me the key combination and the action, I'll fill them in.

```text
Task: Add a keyboard shortcut to this project's UI, following existing UI behavior.

Shortcut: [FILL IN: key combination]
Action it triggers: [FILL IN: the existing UI action or control]

Scope: edits and tests only.

Requirements:
- The shortcut must follow existing UI behavior. Find how the app already handles keyboard shortcuts and how the same action behaves when triggered another way, such as a click. Match that behavior, including the conditions under which it is available or disabled. Reusing existing code is fine but not required.
- Add tests for the new shortcut using the project's existing test setup.

Context:
- You are starting without prior conversation history. Locate the relevant UI code, existing shortcut handling and test setup yourself.
- If the repository has more than one equally plausible place or action for this shortcut, or the fields above are still unfilled, stop and ask which one is meant. Don't pick one yourself.

Verification:
- Run the new tests and the project's existing tests relevant to the changed area.
- In your final report, say what you changed and what the test runs showed. If you couldn't run something, say so plainly.
```

- **Target agent:** none is selected, so the prompt is agent-neutral. I applied no model-specific tuning.
- **Tool access:** I had no terminal or MCP tools, so I didn't inspect any repository. File paths, commands and test frameworks are left for the executor to discover.
- **Authority:** "edits and tests only" is the only scope limit. I didn't add other bans or grants.
- **Reference material:** `guidance.md` is synthetic reference context dated 2026-10-10. No live or official sources were consulted, and the handoff doesn't depend on that file.
- **Review:** I did one self-review pass. It compared each clause in the prompt against your original request, and it found no added requirements.