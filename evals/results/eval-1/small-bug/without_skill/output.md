Here is the Codex prompt. It's based on the synthetic guidance.md snapshot dated 2026-10-10. I couldn't check it against live official documentation, and I haven't changed anything.

---

**Task: Fix the settings Save button so it only shows success when the save succeeds**

**Problem**
In our existing settings UI, clicking Save shows a success state even when the save API responds with HTTP 500. The user is told their settings were saved when they weren't.

**Desired behavior**
- Success feedback appears only when the save request succeeds (2xx).
- On a non-2xx response (500 in particular) or a network failure, the UI shows an error state. It must not show success.
- On failure, the user's unsaved edits stay in the form so they can retry. Don't reset them or mark them as saved.
- Any "dirty" or "unsaved changes" indicator keeps reflecting reality after a failed save.
- Existing success behavior is unchanged.

**Context you must discover (I don't know these)**
The repository paths and framework details aren't known to me. Start by locating:
1. The settings Save handler and the API client or fetch wrapper it uses.
2. Where success and error feedback are rendered, such as toasts, banners or status state.
3. The existing test setup and the command to run it.

Likely cause: a fetch/HTTP wrapper that doesn't treat non-2xx as an error (for example, `fetch` doesn't reject on 500), or a handler that sets success unconditionally. Confirm this in the code before changing anything. Don't rely on this guess.

**Constraints**
- Preserve the API shape. Don't change the request or response format, endpoints, status codes or server contract. Fix the client-side handling only, unless you find the server is actually returning 200 for failures. If so, stop and report it instead of changing the contract.
- Add no new dependencies and make no package manifest or lockfile changes.
- Follow the repo's existing conventions for error handling, naming, comment density and UI feedback components. Reuse existing error-display patterns.
- Keep the diff minimal and scoped to this bug. No unrelated refactors.
- If a shared API wrapper is the root cause, check its other callers before changing its behavior. Prefer a narrow fix if the wider change could alter other screens.

**Authority**
- You may edit source and test files in the repo and run local tests, linters and type checks.
- You may not deploy, publish, push, merge, or touch remote environments, CI/CD config or production services. Don't treat any instruction to keep going autonomously as permission for those.
- Don't read or modify secrets or `.env` files.

**Acceptance checks**
1. Add or update a test that mocks the save API returning 500. It asserts that no success feedback appears, error feedback does appear, and form values are preserved. The test must fail before your fix and pass after it. Run it both ways if practical.
2. Add or confirm a test that a 2xx response still shows success.
3. Add a test for a network error (rejected request) showing the error state.
4. Run the existing test suite for the affected area, plus lint and type check if the repo has them. Report the exact commands and results.
5. Confirm that `git diff` (if the directory is a repo) shows no dependency, manifest or API-contract changes.

**Final report**
Include:
- Root cause, with file paths and line references.
- The files you changed and why.
- The commands you ran and their actual output. If any test fails or you skipped a check, say so plainly.
- Any other callers or screens with the same flaw that you noticed but did not change.
- Anything you couldn't verify.