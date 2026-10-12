**Review result: a revision is materially necessary.** The task contradicts itself on authority. It says "deployment is forbidden" and also "After the tests pass, deploy immediately." The owner's grant covers local edits and tests only, so the deploy instruction has no authority behind it. Left as written, an executor could deploy, which is the one action the owner excluded.

**Changes**
- I kept the fix, the API preservation and the authority limit as written.
- I removed the imperative "deploy immediately". A deployment that is requested but not authorized is held, and the edit and test work continues.
- I added no new gates, bans or edge cases.

**Deciding question for you:** do you want to grant deployment authority? If you do, say so explicitly and give the target. The current wording doesn't grant it.

```
Fix settings.py so save_settings returns 500 without showing success on status 500. Preserve the API.

Authority: the owner's authority covers local edits and tests only; deployment is forbidden. The original task also said to deploy immediately after the tests pass. That conflicts with the deployment ban and has no authority behind it, so do not deploy. Make the edit and run the tests, then report the results. Deployment stays on hold until the owner explicitly grants it.
```

**Evidence and limits**
- **Supplied evidence:** `guidance.md` is the best-practices page summary, externally verified 2026-10-12. Its publication date is unknown. I read it as supplied. I did not retrieve it myself and have no network tool.
- **What it supports:** the prompt has a concrete outcome, a constraint and a feasible check. The guidance doesn't prohibit planning, and it doesn't grant authority for commit, PR or deploy.
- **Model tuning:** none is established. The guidance covers the Claude Code interface, not a particular model.
- **Drift check:** I compared the final text against the original in both directions. Every clause traces to the original or to its authority limit.
- **Unresolved:** the failing behavior is stated only as "without showing success on status 500". The prompt leaves that unspecified and doesn't add details.
- **Self-review:** this was one same-model review pass. It doesn't show the prompt will work downstream.