The original prompt is already suitable. No material revision is necessary.

**Contract check against your words**
- Goal: "Fix settings.py so save_settings returns 500 without showing success when the API returns status 500." The prompt states this directly.
- Invariants: "Preserve the request payload and the status-200 success behavior" and "No new dependencies" are both explicit constraints. "No new dependencies" doesn't freeze manifests, and the prompt doesn't claim it does.
- Authority: "Local edits and tests are authorized; do not commit or deploy." Edit and test authority is granted, and commit and deploy are forbidden. Nothing is added or dropped.
- Acceptance: "Verify both 500 and 200 behavior using the existing tests and report actual results." These checks test the requested behavior and its regression, and they require reporting real output. They add no invented gates such as coverage thresholds or a new test framework.
- Process: the prompt doesn't dictate a mechanism, ban planning, or add edge-case mandates like handling all network errors. The file path is named, so there is no ambiguity about the target. Any missing detail, such as how the 500 currently shows success, is ordinary discovery for the executor.

**Fresh executor**
The prompt is short and self-contained. It doesn't depend on chat history.

**Optional addition (not needed)**
If the existing tests don't cover the 500 case, the executor will have to decide whether to add one. Your wording ("using the existing tests") leaves that open, and I left it open too.

**Freshness**
`guidance.md` is a synthetic fixture dated 2026-10-10, and no network or official retrieval was available. I used it only as dated test context. This review doesn't rely on current official guidance, and the executor's model is unestablished.

I did not execute the task.