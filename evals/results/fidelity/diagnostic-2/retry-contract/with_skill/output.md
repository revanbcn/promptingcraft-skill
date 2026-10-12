Below is the handoff. The user's message doesn't say what the worker currently does wrong, so I left the expected behavior for `failed_final` jobs open instead of guessing. The only reference I had was an offline, dated fixture (2026-10-10), and I did not claim any live official sources. The executor's repo, test commands and MR tooling are unknown, so the prompt tells the executor to discover them.

```
Repair the worker that retries jobs after a terminal failure. Terminal means status equals failed_final.

Context
- You don't have the chat that produced this request. The repo, worker code, tests and tooling are for you to discover; no file paths or commands are given here.
- The request doesn't describe the exact faulty behavior. Work it out from the worker code, its tests and any logs or fixtures in the repo. If the intended behavior for failed_final jobs is still ambiguous after that, say so in your report instead of guessing silently.

Constraints
- Preserve job IDs.
- Preserve the existing retry schedule for other statuses.
- Do not add dependencies.
- Do not change the database schema.
- Monitoring improvements are not part of this fix.

Authority
- Authorized: edits, local tests, and a draft MR.
- Not authorized: merge and deploy.

Verification
- Run the relevant local tests. Add or adjust tests only as needed to show the failed_final behavior is fixed and that retries for other statuses, and job IDs, are unchanged.
- In your final report, include the test commands you ran and their results. State plainly anything you could not run or verify.

Optional suggestion (not part of the fix, not an acceptance criterion): after the fix, list any monitoring improvements you think would help, in a separate section of your report. Don't implement them.
```

- **Open question:** whether `failed_final` jobs should be skipped entirely or handled some other way. The prompt leaves that to the executor and asks for a flag if the code doesn't settle it.
- **Authority:** it carries over the edits, local tests and draft MR you authorized. It doesn't grant anything extra, and it holds only merge and deploy.
- **Monitoring:** it appears only as a visibly optional suggestion, not as part of the fix or a completion check.