Here is the handoff. The target is Codex, and the executor model is unestablished, so I used agent-level guidance only. Offline, `guidance.md` and the Codex notes are dated cached context (fixture 2026-10-10), not live-verified. I did not include `guidance.md` in the prompt.

```text
Fix a bug in our existing settings UI: Save shows a success state after the API returns a 500 response.

Context
- This is user-reported. Reproduce it first, then fix it. The correct behavior is that a 500 response from Save is not presented as success.
- I don't know the exact repository paths. Locate the settings UI's Save flow and the code that calls the save API yourself.
- I haven't specified what the user should see after a 500. Follow the UI's existing error-handling behavior where one exists.

Constraints
- Preserve the API shape.
- Add no new dependencies.

Authority
- You may edit files and run tests.
- Do not deploy. Deployment is not authorized.

Verification
- Add or update a test, using the repository's existing test setup, showing that a 500 response from Save no longer shows success. Run it and the relevant existing tests.
- Report what you changed and the actual test output. If a test fails or you couldn't run one, say so.

Optional suggestion: if the success path also has coverage, keep it passing to confirm a successful Save still shows success.
```

Notes:
- I kept your wording for the constraints and authority: preserve the API shape, no new dependencies, edits and tests authorized, no deployment. "Preserve the API shape" is unconditional.
- I did not specify the 500 error UI, any handling of other failures, or a ban on commits. You didn't state any of these.
- Unknown paths are left to the executor to discover. I treated them as ordinary discovery, not as a choice between several candidate targets.
- The test check only tests the reported bug (a 500 must not show success).