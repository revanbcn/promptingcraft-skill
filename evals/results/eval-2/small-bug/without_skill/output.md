Here is the prompt, ready to paste into Codex. It follows the fixture guidance (snapshot 2026-10-10, synthetic, not live-verified official guidance). It states the behavior, context, constraints, authority and acceptance checks, because the executor can't see this chat.

---

**Task: Fix the settings Save button so it doesn't report success after a failed API call**

**Problem**
In our existing settings UI, clicking Save shows a success message even when the save request returns HTTP 500. A failed save must be shown as a failure. The user must not be told their settings were saved when they weren't.

**Context you don't have**
- I don't know the repository layout, framework, or the file paths. Find the settings page and its save handler yourself. Search for terms like `settings`, `save`, `onSave`, `handleSubmit`, and the success toast or notification text.
- I don't know the test runner or tooling. Infer them from the repo's config files (`package.json`, `pyproject.toml`, `Makefile` and similar) and its existing tests.
- Before editing, tell me what you found: the files involved, the cause of the bug, and the test command you plan to use. The likely cause is a handler that ignores the response status, for example `fetch` without a `response.ok` check, a `catch` that swallows the error, or success state set before the await resolves. Confirm this in the code and don't assume it.

**Desired behavior**
- If the save API returns a non-2xx status (500 in particular), or the request throws, such as on a network error, the UI shows the existing error state or message pattern. It must not show the success message.
- On failure, the user's unsaved edits stay in the form so they can retry. Any "saved" or "dirty" indicator must not be reset.
- On a 2xx response, the behavior is unchanged.
- Any loading or disabled state on the Save button is cleared in both the success and failure cases.
- If the UI has no error pattern, reuse the closest existing one, such as a toast, banner, or inline message. Keep any new user-facing text minimal and consistent with the surrounding copy.

**Constraints**
- Preserve the API shape. Don't change the endpoint, HTTP method, request payload, response format, or any server-side contract. Keep the fix on the client side unless you find the server is wrongly returning success. In that case, stop and report it instead of changing it.
- Add no new dependencies. Don't edit lockfiles or dependency manifests.
- Keep the diff small and focused on this bug. Do no unrelated refactors, reformatting, or renames.
- Match the surrounding code's style, naming, and comment density.

**Authority**
- You may edit source files and add or update tests, and you may run the test suite, linter, and type checker locally.
- You may not deploy, publish, merge, push, or change CI or infrastructure configuration. Running autonomously doesn't grant any of these permissions.
- Don't make network calls beyond what the local tests already require. Don't touch secrets or environment files.

**Acceptance checks**
1. Add or update a test that mocks the save API returning 500. It must assert that the success message is not shown, that the error state is shown, and that the form values are retained. Confirm this test fails before your fix and passes after it. If a failing run isn't practical, say so.
2. A test, existing or new, covers a 2xx response and still shows success.
3. A test or an explicit check covers a thrown or network error. It must not show success.
4. The relevant existing test suite, linter, and type checker pass. If any can't run, or any fail for reasons unrelated to your change, say so and include the output.
5. The request payload and endpoint are unchanged. Your final report should confirm this by pointing to the unchanged lines.

**Final report**
Include:
- The root cause.
- The files changed and a short summary of each change.
- The exact commands you ran, with pass or fail results.
- Anything you couldn't verify.
- Any server-side concerns you noticed but didn't change.

Do not claim the fix is verified unless you actually ran the tests.

---

I wrote it to work with any executor model, since the model is unknown. I haven't run or implemented anything.