```
Fix a bug in our existing settings UI: clicking Save shows a success state even when the save request returns HTTP 500. Make the UI report failure when the API call fails.

Context
- I don't know the repository layout. Find the settings page and its save handler yourself, along with the API client code it uses and any existing tests.
- Follow the existing code's conventions for state, error display and tests.

Required behavior
- On a 500 response, or any non-2xx response or network error, don't show success. Show an error state using the UI's existing error or notification pattern. If it has none, add the smallest consistent one.
- Keep the user's unsaved edits in the form so they can retry. Don't mark the form as clean or saved.
- Success behavior on a 2xx response must stay unchanged.
- Find out why success was shown (for example, the response status is never checked, or errors are swallowed) and fix that cause. Don't just patch the symptom.

Constraints
- Preserve the API shape. Don't change request or response formats, endpoints, or status-code semantics, and don't change the server unless you find it is itself mishandling the request. If you think an API change is needed, stop and report it instead of making it.
- Add no new dependencies and make no lockfile or package manifest changes.
- Keep the diff narrow. Do no unrelated refactors.

Authority
- You may edit files and run local tests, linters and type checks.
- Do not deploy, publish, merge or push. Do not run release or deploy scripts, and don't trigger CI that deploys.

Acceptance
- Add or update a test that mocks a 500 response and asserts the UI shows an error, doesn't show success, and keeps the user's edits. Confirm it fails before your fix and passes after, if that is practical.
- Add or keep a test showing that a 2xx response still shows success.
- Run the project's existing test, lint and type-check commands that are relevant. Find them in the repo's scripts or docs. Don't invent commands.

Final report
- List the files changed, the root cause, the exact commands you ran with their results, and anything you couldn't verify or that you assumed. If a check failed or was skipped, say so plainly.
```

Notes:
- I wrote this for Codex. The model is unknown, so I added no model-specific tuning, and I left the repository paths for the executor to find.
- I only had `guidance.md`, a synthetic fixture dated 2026-10-10, and no network access. I treated it as dated test context, not live official guidance. I followed its advice to state behavior, constraints, authority and acceptance checks.
- Edits and tests are authorized. Deployment, merge and push are explicitly held back.
- The instructions to keep unsaved edits and to use the existing error pattern are my own assumptions, which the executor may adjust. You didn't ask for them. Remove them if you want a stricter scope.