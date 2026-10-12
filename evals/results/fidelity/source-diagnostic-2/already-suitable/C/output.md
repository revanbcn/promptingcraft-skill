The original prompt is already suitable. No material revision is necessary.

**Contract check**
- **Goal:** `save_settings` must return 500 and must not show success when the API returns status 500.
- **Constraints:** the request payload and the status-200 success behavior stay as they are, and no new dependencies are added.
- **Authority:** local edits and tests are authorized. Commit and deploy are forbidden, and the prompt adds no other grants or bans.
- **Verification:** it asks for both the 500 and 200 paths to be checked with the existing tests and for actual results to be reported. That tests the requested behavior directly, adds no new completion criteria, and doesn't require new tests or a coverage target.

**Residual notes**
- **Locating `settings.py`:** the prompt doesn't give a path, so the executor will find it by ordinary discovery. If several `settings.py` files exist, the executor should ask which one.
- **Process left open:** the prompt doesn't say whether to plan first. That is correct, since the user didn't choose, and the Claude Code guidance treats a small-diff shortcut as conditional rather than required.
- **Not established:** I haven't confirmed that the executor has existing tests that cover both paths. If it finds none, it should report that instead of inventing a gate.
- **Source freshness:** the `guidance.md` retrieval (best-practices page, externally verified 2026-10-12) was supplied to me. I didn't fetch it myself, and its publication date is unknown. The guidance supports this conclusion but doesn't show the prompt will work downstream.