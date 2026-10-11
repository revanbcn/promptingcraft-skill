Here is the Codex prompt:

```
Fix a bug in our existing settings UI: after the user clicks Save, the UI shows a success state even when the settings API responds with HTTP 500. A failed save must be reported as a failure.

Context
- You are working in the repository you were started in. I don't have exact file paths, so locate the settings page, its Save handler, and the API client call it uses.
- Reproduce the bug first (a failing test or a minimal demonstration) before changing anything.

Required behavior
- On a non-2xx response (500 in particular) or a network failure, don't show the success state. Show the UI's existing error pattern, using existing components and copy conventions. Keep the user's unsaved edits in the form so they can retry.
- On 2xx, behavior stays exactly as it is today.
- Don't leave the form marked as saved or clean after a failure. Re-enable Save so the user can retry.

Constraints
- Preserve the API shape: don't change request or response formats, endpoints, status codes, or server contracts. The fix belongs in the client's handling of the response.
- Add no new dependencies.
- Keep the change minimal and match the surrounding code style. Don't refactor unrelated code.

Authority
- You may edit files and run tests, linters and type checks, using the repo's existing commands.
- Don't deploy, publish, merge, or push. Don't change CI or release configuration. Stop at a local, reviewable change.

Acceptance
- A test, added in the repo's existing test framework, fails before the fix and passes after it. It covers a 500 response (no success shown, edits kept) and a 2xx response (success shown).
- The existing relevant test suite, lint and type checks pass. If you can't run one, say so and say why.
- In your final report, give the root cause, the files changed, the exact commands you ran with their results, and any assumptions or remaining risks. Don't claim success without that output.
```

**Notes**
- **Sources:** I used `guidance.md`, a synthetic fixture dated 2026-10-10, and the skill's Codex notes dated 2026-10-12. No live retrieval was possible, so I make no claim about current official guidance.
- **Executor model:** it's unknown, so the prompt has no model-specific tuning.
- **Assumptions:**
  - The "existing error pattern" and "keep edits" behaviors are my bounded defaults. Remove them if your UI should behave differently.
  - The prompt doesn't name test commands or file paths, because I don't know them. It tells the executor to discover them.
- **Authority:** edits and tests are granted. Deployment, merging and pushing are explicitly held.