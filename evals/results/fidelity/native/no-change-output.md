Task contract:

- **EXPLICIT_REQUIRED:** Fix `settings.py` so `save_settings` returns 500 without showing success when the API returns 500. Preserve the request payload and status-200 success behavior. Verify both statuses using existing tests and report actual results.
- **EXPLICIT_REQUIRED authorization:** Local edits and tests.
- **FORBIDDEN:** New dependencies, commits, deployment.
- **UNRESOLVED:** Target agent/model and test commands are unspecified; neither blocks this handoff.
- This review is authoring only; execution authorization belongs to the future executor.

Critique: The prompt clearly states the bug, preservation constraints, verification, and action boundaries. No material omission, contradiction, or unsupported requirement was found. Additional process instructions or broader error handling would expand its scope. This was self-review, not independent verification.

Freshness: Packaged guidance records retrieval on **2026-10-12**. It is **dated cached**, within its stated seven-day refresh window, and was not live-verified. No model-specific guidance was assumed.

**The original prompt is already suitable. No material revision is necessary.**

`task.txt` remains unchanged. No development task or tests were executed.