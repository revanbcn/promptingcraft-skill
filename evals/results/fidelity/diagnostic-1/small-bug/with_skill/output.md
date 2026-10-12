Here is the prompt, ready to paste into Codex.

```
Fix a bug in our existing settings UI: Save shows a success state after the API responds with a 500. After the fix, a 500 response from the Save request must not be shown as success.

Context
- You are starting fresh and have no access to the chat that produced this prompt. Find the settings UI's Save flow and the API call it makes in the repository. I don't know the exact paths.
- If the code has more than one plausible Save flow or settings screen, and you can't tell which one the report means, stop and ask me which one. Don't pick one.
- The executor model is unknown, so use your normal working approach.

Requirements
- A 500 API response must no longer produce the success outcome in the settings UI.
- Preserve the API shape. Don't change the API's request or response contract.
- Add no new dependencies.

Authority
- You may edit code and add or run tests.
- Do not deploy.

Verification
- Show observable evidence that a 500 response from Save no longer shows success. For example, run a test that failed before the fix and passes after it.
- Report which tests you ran and their results. If you could not run something, say so plainly.

Optional suggestion: follow the repository's existing conventions for how the UI shows a failed save, if it has any.
```

**Notes on what I did**
- **Contract:** I kept your four constraints as stated: the 500-after-success bug, preserve the API shape, no new dependencies, and edits and tests authorized with deployment not. I didn't add bans on commits or on dependency manifests, because you didn't ask for them.
- **Unknowns:** The prompt tells Codex to discover the paths. If it finds several plausible Save flows, it asks you instead of guessing. I didn't invent a failure-message design or handling for other errors. The error-display convention is only an optional suggestion.
- **Source freshness:** Network retrieval was unavailable, so nothing here is live-verified. I used `guidance.md` (a synthetic fixture dated 2026-10-10) and the skill's offline Codex notes (checked 2026-10-12). Both are dated cached context, not official guidance. Model-specific tuning is not established, since the executor model is unknown.
- **Checks:** I compared the final text against your request in both directions and found no added mandates. The verification section only checks the requested behavior. This was self-review, not independent verification.