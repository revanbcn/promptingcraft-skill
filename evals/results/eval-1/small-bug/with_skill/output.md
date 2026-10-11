Here's the execution prompt. I didn't load the skill's `references/` notes, so no Codex-specific tuning is applied. The only guidance I used is `guidance.md`, a synthetic fixture dated 2026-10-10. It is not live-verified or official, and no network retrieval was available. I wrote the prompt for a generic Codex-style executor because the model is unknown. Plan mode was active, so I made no edits and ran no commands.

```text
Task: fix the settings UI so Save no longer reports success when the save API returns a 500 response.

Context
- In our existing settings UI, clicking Save shows a success state even when the API responds with HTTP 500. I haven't confirmed the cause. It may be missing status checking, a swallowed error, optimistic UI, or a success path that runs regardless of outcome. Find the actual cause and don't assume.
- I don't know the exact repository paths, framework, or test setup. Locate the settings UI, its Save handler, and the API client code it calls by searching the repo. Follow the existing code's conventions and its existing test tooling.
- You can't see my chat history, so everything you need is in this prompt.

Desired behavior
- If the save request fails (a 500, and any other non-2xx or network failure on the same path), Save must not show success. It must show the app's existing error treatment, or the closest equivalent. Don't invent a new design system or pattern.
- The user's unsaved edits stay in the form after a failure, so they can retry.
- A successful save still shows success, and its behavior doesn't change.
- Any loading or disabled state on Save resets after a failure, so the user can retry.

Constraints
- Preserve the API shape. Don't change request or response formats, endpoints, status codes, or server contracts. This is a client-side fix unless you find the server is mislabeling its own responses. If so, stop and report that instead of changing the server contract.
- Don't add any new dependencies, and don't change the lockfile or package manifests.
- Keep the change minimal and local. No unrelated refactors, renames, or formatting churn.

Authority
- You may edit code and add or update tests in the repo, and you may run local tests, linters, and type checks.
- Deployment is not authorized. Don't deploy, publish, push to remote environments, merge, or run release commands. Prepare and verify the change locally only.
- Don't read or expose secrets or credentials. Don't call external services. If reproducing the failure needs a live backend, mock the API in tests instead.

Acceptance checks
1. Add or update an automated test that fails before your fix and passes after it. It must mock a 500 from the save call and assert that the success state is not shown and the error state is shown. Use the repo's existing test framework and mocking approach.
2. Add or confirm a test that a successful save still shows success.
3. Run the relevant existing test suite for the settings area, plus lint and type checks if the repo has them. Report the exact commands and their results. If something can't run, say so and why. Don't claim a pass you didn't observe.
4. Confirm that no API request or response shape changed and that package manifests and lockfiles are unchanged.

Completion report
- Root cause, in a few sentences.
- Files changed, with a one-line reason for each.
- Test commands run and their actual outcomes, including any failures or skipped checks.
- Assumptions made, and anything left unresolved, such as other Save-like flows with the same bug that you noticed but didn't change.

If you hit a blocker that changes scope (for example, the fix would require an API change), stop and report it instead of working around it.
```

- **Assumptions:** the bug is client-side, a failure should use the app's existing error pattern, and edits should be preserved on failure. Each is stated in the prompt as a bounded expectation, so the executor doesn't have to ask.
- **Authority:** edits and tests are granted. Deployment, merge, and push are explicitly withheld, and "continue autonomously" is not treated as permission for any of them.
- **Self-review:** I did one pass against the contract. Every constraint you gave is kept, and I added no approvals or scope.