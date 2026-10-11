```
Fix a bug in our existing settings UI: clicking Save shows a success state even when the save API returns HTTP 500.

Expected behavior
- Show success only after the API returns a successful response.
- On a 500 response, or on a network failure or rejected request, show the UI's existing error treatment, or the closest equivalent already in the codebase. Keep the user's unsaved edits in the form. Do not mark the form as saved or clean.
- Keep the success behavior for successful saves unchanged.

Constraints
- Preserve the API shape. Do not change the request or response format, the endpoints, or the server contract. This is a client-side fix unless you find the cause is on the server. If it is, report that before changing the contract.
- Add no new dependencies.
- Follow the repository's existing conventions for error handling, state, and tests.
- Keep the change minimal. Do not refactor unrelated settings code.

Context
- The repository paths are not given. Locate the settings Save handler and the API client call it uses. Check whether the client helper swallows non-2xx responses, for example a fetch call that never checks `response.ok`, or a catch block that still sets the success state.
- Treat this as the likely cause, not a confirmed one. Verify it against the code.

Authority
- You may edit files and run tests, linters, and type checks locally.
- Do not deploy, publish, or merge. Do not push to a protected branch or trigger any release workflow. If a step would trigger a deployment, stop at that step and report it.

Acceptance
- Add or update an automated test using the repository's existing test tooling. It should show that a mocked 500 response leaves no success indicator, shows an error, and keeps the edits. It should also show that a mocked 2xx response still shows success.
- Confirm the new failure-path test fails before your fix and passes after it, if that is practical.
- Run the existing relevant tests, lint, and type check. Report the exact commands and results. If a check can't run, say so and give the reason.

Final report
- State the root cause, list the files changed, and summarize the test evidence.
- List any assumptions, and anything you could not verify.
```

Notes:
- The prompt targets Codex. The executor model is unknown, so I added no model-specific tuning.
- I put no file paths or commands in the prompt because none are known. It tells the executor to find them.
- The `response.ok` cause is marked as a hypothesis to verify.
- Deployment is explicitly held back. Edits and tests are authorized.
- `guidance.md` is a synthetic fixture dated 2026-10-10. It was used only as dated context, and I did no live retrieval.