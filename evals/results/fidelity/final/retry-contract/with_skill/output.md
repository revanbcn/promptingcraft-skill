Here is the handoff. I composed it only, and nothing was run or edited.

```text
Repair the worker that retries jobs after a terminal failure.

Reported problem (user-reported; reproduce it before changing code): the worker retries jobs after a terminal failure. Terminal means status equals failed_final.

Constraints:
- Preserve job IDs.
- Preserve the existing retry schedule for other statuses.
- Do not add dependencies.
- Do not change the database schema.

Authority:
- Authorized: edits, local tests, and a draft MR.
- Not authorized: merge and deploy.

Context: you start without this conversation's history. The repository, worker location and test setup are not specified, so find them in the repo. If more than one worker plausibly matches, stop and ask which one is meant.

Verification: add or run a local test showing that a job with status failed_final is no longer retried, and that the retry schedule and job IDs for other statuses are unchanged. In your final report, include the test evidence and the draft MR link.

Optional suggestion: if you notice useful monitoring improvements, list them separately in your final report. They are not part of this fix, so do not implement them.
```

Notes:
- **Assumption:** I read "repair the worker that retries jobs after a terminal failure" as "jobs in `failed_final` should not be retried." The prompt keeps your wording and tells the executor to reproduce the failure first, so it doesn't commit to a mechanism. If you meant a different intended behavior, such as a different handling of those jobs, tell me and I'll adjust the prompt.
- **Left open:** I didn't add a file path, a test command or a planning instruction, because none were given. Only an ambiguous worker target triggers a question.
- **Authority:** I kept your grants exactly as stated and added no extra bans, such as on commits.
- **Executor model:** unknown, so I used general Claude Code guidance: outcome, constraints, and a check the executor can run.
- **Sources:** `guidance.md` is a synthetic fixture dated 2026-10-10, so I treated it as dated test context. It is not live official guidance, and I did not retrieve anything from the network. I did not pass the file to the executor.