**Verdict: no material revision needed.** The task is small and already carries the full contract, so I left the wording as is.

I compared it with your original in both directions:
- **Required items:** each one is present with its original strength.
  - Fix `save_settings` so it returns 500 without showing success when the API returns 500.
  - Preserve the request payload.
  - Preserve the status-200 success behavior.
  - Add no new dependencies.
  - Verify both the 500 and 200 cases with the existing tests, and report actual results.
- **Authority:** local edits and tests are authorized. Committing and deploying are excluded, and the prompt grants nothing beyond that.
- **Added requirements:** there are none. I didn't add handling for other network errors, new tests, coverage targets or timeouts.
- **Fresh-executor context:** the prompt names the file and function, and the executor can find them itself. I didn't invent paths or test commands I can't confirm.

**Sources:** I used the skill's dated offline notes and the synthetic `guidance.md` (snapshot 2026-10-10). Nothing was live-verified, and no network retrieval was used. The target is Claude Code, but its model isn't established, so I applied no model-specific tuning. This was a single self-review pass, not independent verification. I composed the prompt only and did not touch `settings.py` or run any tests.

```
Fix settings.py so save_settings returns 500 without showing success when the API returns status 500. Preserve the request payload and the status-200 success behavior. No new dependencies. Local edits and tests are authorized; do not commit or deploy. Verify both 500 and 200 behavior using the existing tests and report actual results.
```