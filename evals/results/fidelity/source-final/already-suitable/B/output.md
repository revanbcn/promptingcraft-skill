The original prompt is already suitable. No material revision is necessary.

**Review findings**
- **Coverage:** The prompt keeps every requirement in the original task:
  - Fix `settings.py` so `save_settings` returns 500 and shows no success on an API 500.
  - Preserve the request payload and the status-200 success behavior.
  - Add no new dependencies.
  - Local edits and tests are authorized.
  - Do not commit or deploy.
  - Verify the 500 and 200 behavior with the existing tests, and report actual results.
- **Authority:** Edit and test permission is stated and limited to local work. The commit and deploy bans are the user's own. No grants were added or dropped.
- **Added behavior:** Nothing extra is required. It doesn't ask for handling of other errors, new tests or a coverage gate. It also doesn't freeze files other than by the no-new-dependencies rule.
- **Verification:** The 500 and 200 checks test exactly the requested behavior. "Report actual results" asks for real output rather than a claimed pass.
- **Context:** `settings.py` is named, and its location can be found by searching. There's no ambiguity over which file or function is meant, so no question is needed.
- **Process:** It doesn't forbid or require planning, so the executor can choose.

**Assumptions and freshness**
- **Target and model:** I treated the executor as Claude Code, but its model isn't established, so I applied no model-specific tuning.
- **Guidance:** `guidance.md` is dated synthetic context (2026-10-10). No live retrieval was available. The Claude Code notes are dated cached guidance, not current official guidance.
- **Not run:** I didn't execute the task. This review doesn't show the fix will work.