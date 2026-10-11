Here is the handoff for Claude Code.

```
Task: fix the worker that retries jobs after a terminal failure.

Context
- "Terminal" means a job whose status equals `failed_final`. The retry worker currently retries these jobs after a terminal failure, and that is the bug. The worker should not retry them.
- You have no chat history. Find the retry worker and its tests in the repo yourself. Confirm the root cause by reading the code and reproducing the bug before you change anything.

Required behavior
- A job with status `failed_final` must never be retried or rescheduled by the worker.
- Jobs with any other status keep their existing retry schedule exactly as it is now: same timing, same backoff, same attempt limits.
- Job IDs must be preserved. Do not regenerate, reassign or recycle them, and do not create replacement jobs.

Constraints
- Do not add dependencies.
- Do not change the database schema. That includes migrations.
- Keep the change minimal and match the surrounding code's style.
- Monitoring, alerting and logging improvements are not part of this fix. Do not implement them. If you have ideas, list them in a separate "Suggestions" section of your final report.

Authority
- Allowed: edit code, run local tests, and open a DRAFT merge request.
- Not allowed: merge the MR or deploy. If a pipeline or release workflow would deploy automatically on merge, leave the MR as a draft and do not merge it.

Acceptance (run locally and show the output)
1. A test fails before the fix and passes after it: a `failed_final` job is not retried.
2. A regression test or existing tests show that other statuses still follow the unchanged retry schedule.
3. A test or assertion shows job IDs are unchanged.
4. The existing test suite passes. If you can't find or run it, say so plainly instead of claiming it passed.

Final report
- Root cause, files changed, test commands and results, and the draft MR link.
- Anything you could not verify.
- Suggestions (separate and optional).
```

- **Assumptions:** I didn't name files, test commands or the MR target, because none were given. The prompt tells the executor to find them.
- **Authority:** Nothing was added beyond what you authorized. Merge and deploy are explicitly held back.
- **Sources:** `guidance.md` is a synthetic fixture dated 2026-10-10. Nothing was verified live, because network retrieval is unavailable. The Claude Code notes I used are dated, cached guidance, not live-verified.