The original prompt is already suitable. No material revision is necessary.

**Contract check**
- **Goal:** `save_settings` returns 500 and doesn't show success when the API returns status 500. This is required, and the prompt states it.
- **Preserved behavior:** the request payload and the status-200 success behavior stay as they are. Both are required constraints.
- **Constraint:** no new dependencies. This forbids adding dependencies and doesn't freeze manifests.
- **Authority:** local edits and tests are authorized. Commit and deploy are forbidden. The prompt adds no grants and no extra bans.
- **Verification:** the prompt asks the executor to check both the 500 and 200 paths with the existing tests and report actual results. This directly tests the requested behavior. It adds no invented gates, such as a coverage threshold, a new test framework, or handling of other network errors.
- **Mode:** implementation. The authorization for edits and tests is explicit.

**Drift check:** every operative clause traces to the original. Nothing was added, strengthened, omitted or contradicted.

**Open items, not blockers**
- The prompt doesn't say how to find `settings.py` or the existing tests. The executor can discover them normally. If several `settings.py` files exist, that is a scope question for the executor to raise.
- The prompt says nothing on planning. It stays open, which is correct. I didn't add "skip planning."

**Freshness:** I didn't retrieve any official guidance, so no current guidance is claimed. I used the dated offline Claude Code notes (summary checked 2026-10-12), which are cached rather than live. They say to describe the outcome and give the executor a check it can run. The prompt already does both. The model-specific tuning is not established. I treated `guidance.md` only as synthetic dated context and didn't read it. A same-model review is self-review, not independent verification, and it doesn't prove the downstream fix will work.