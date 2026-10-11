Here is the Codex handoff. The task is small, so the prompt is too.

```text
Fix a bug in our existing settings UI: after the Save request gets a 500 response from the API, the UI still shows a success state. A failed save must not be presented as a success.

Context
- The repository paths for the settings UI and its save call are not known to me. Find them in the repository you're working in.
- Reproduce the bug first: make Save receive a 500 response and confirm the UI shows success.
- What the UI should show instead of success is not specified. Use the app's existing conventions for showing errors if it has them. Otherwise pick the smallest reasonable behavior and say what you chose.

Constraints
- Preserve the API shape. Don't change request or response formats, endpoints or status codes.
- Don't add new dependencies.

Authority
- You may edit code and add or run tests in the repository.
- You may not deploy. Don't run any deployment, release or publish step. If a merge or push would trigger a deployment, don't do it.

Verify
- Show evidence, such as a test or a reproduction run, that a 500 response from Save no longer produces a success state.
- Run the relevant existing tests and report the results. Report any failures with their output.

Final report: list the files changed, summarize the fix, give the test results, and note anything you could not verify.
```

- **Open choice kept open:** you didn't say what the UI should show after a failed save, so the prompt leaves that to the executor and asks it to report what it chose.
- **Paths and model:** the paths are left for the executor to find. Because the executor model is unknown, I used general Codex guidance and no model-specific tuning.
- **Sources:** `guidance.md` is a dated fixture (2026-10-10), and Codex notes were checked 2026-10-12. Neither is live-verified, because network retrieval was unavailable.
- **Self-review:** I compared the final clauses against your original request in one pass. That is self-review, not independent verification.