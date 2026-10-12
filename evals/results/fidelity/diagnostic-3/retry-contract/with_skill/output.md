```
Repair the worker that retries jobs after a terminal failure. Terminal means status equals failed_final.

Context: This is a user-reported defect. Reproduce it first, then fix it. You don't have this chat history, and I haven't given you file paths, so find the worker and its tests in the repository.

Requirements:
- Preserve job IDs.
- Preserve the existing retry schedule for other statuses.
- Do not add dependencies.
- Do not change the database schema.

Authority:
- You may edit files, run local tests, and open a draft MR.
- You may not merge or deploy.

Verification: Run the relevant local tests. Show that a job with status failed_final is no longer retried, that job IDs are unchanged, and that jobs with other statuses keep their current retry schedule. Report what you ran and the results. If a test fails or you skip a check, say so.

Optional suggestion: If you see useful monitoring improvements, list them separately in your final report. They are not part of this fix, so don't implement them.
```

Notes:
- I read "retries jobs after a terminal failure" as the user-reported defect. The prompt doesn't spell out the desired behavior beyond that, so the executor has to reproduce the failure and confirm it.
- The prompt doesn't restrict commits or manifest and lockfile changes. "No new dependencies" only forbids adding dependencies.
- I did not pass `guidance.md` to the executor. It is author-side reference material.
- Guidance freshness: no network was available. The only guidance I had was the dated cached Claude Code notes (summary checked 2026-10-12) and the synthetic fixture snapshot (2026-10-10). Neither is live-verified, and the model behind the executor is unestablished.
- Drift check: every operative clause traces to your request. The verification line only checks the requested outcomes. The monitoring line is marked optional and isn't a completion gate.