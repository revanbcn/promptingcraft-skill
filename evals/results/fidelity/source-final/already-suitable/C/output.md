The original prompt is already suitable. No material revision is necessary.

I checked each requirement against the original wording, and each is stated clearly and with its intended strength:
- **Goal:** `save_settings` in `settings.py` returns 500 and doesn't show success when the API returns 500.
- **Invariants:** the request payload and the status-200 success behavior stay as they are.
- **Dependencies:** no new dependencies.
- **Authority:** local edits and tests are allowed. Committing and deploying are not.
- **Verification:** the 500 and 200 behavior are checked with the existing tests, and the actual results are reported.

Nothing needs correcting:
- **Authority:** it is explicit, and the prompt neither adds nor drops a grant.
- **Process:** it doesn't forbid planning, and it doesn't invent a mechanism, a retry or timeout behavior, or other error handling.
- **Completion check:** it tests exactly the requested behavior. It also asks for actual results, which fits an executor that can run the tests.
- **File location:** `settings.py` is a plain file name the executor can find on its own. I didn't see any competing targets.
- **Shape and size:** this is a small, clear fix, so the prompt can stay as short as it is.

On sources: `guidance.md` is the supplied summary of the Claude Code best-practices page, externally verified 2026-10-12. I didn't retrieve anything myself, and I have no network tool. That guidance fits the prompt: context, constraints and a runnable check. It doesn't establish how well the prompt will work with any particular model. I haven't run the task or looked at the code or tests.

**Prompt (unchanged):**

```
Fix settings.py so save_settings returns 500 without showing success when the API returns status 500. Preserve the request payload and the status-200 success behavior. No new dependencies. Local edits and tests are authorized; do not commit or deploy. Verify both 500 and 200 behavior using the existing tests and report actual results.
```