Here's the handoff. The task text gives no repo path, worker name or test command, so the prompt tells the executor to find them instead of naming any.

```
Repair the worker that retries jobs after a terminal failure. Here, "terminal" means the job's status equals `failed_final`. The worker should no longer retry a job once it is in that status.

Context
- You are starting without my chat history. Locate the retry worker and its status handling in the repository yourself. I haven't given you a file path, test command or branch name.
- I haven't said how the bug shows up or what its root cause is. Establish that from the code before changing it.

Constraints
- Preserve job IDs. The fix must not change, regenerate or reassign them.
- Keep the existing retry schedule unchanged for every status other than `failed_final`.
- Do not add dependencies.
- Do not change the database schema.
- Keep the change limited to this fix. Monitoring improvements are not part of it.

Authority
- Allowed: editing files, running tests locally, and opening a draft MR.
- Not allowed: merging the MR and deploying. Leave both for me, even if a pipeline or release process would do them automatically. If a step would trigger a merge or deploy, stop before it and continue only with the allowed work.

Done when you can show evidence, from local tests or a direct check, that:
- a job with status `failed_final` is not retried;
- jobs with other statuses are retried on the same schedule as before;
- job IDs are unchanged.
Report what you ran and what the results were. If something could not be run or verified, say so plainly. Then give me the draft MR link or description.

Optional suggestion, not part of this fix and not a completion requirement: if you notice monitoring or alerting gaps around terminal failures, list them separately in your final report. Do not implement them.
```

- **Contract kept:** the terminal definition, ID preservation, the unchanged schedule for other statuses, the no-dependencies and no-schema constraints, and the edit/test/draft-MR authority all carry over. Merge and deploy stay forbidden, including when something would trigger them automatically.
- **Inferred reading:** I read "repair the worker that retries after a terminal failure" as "stop retrying `failed_final` jobs". If you want a different outcome for those jobs, such as a specific final state or a notification, say so before sending.
- **Monitoring:** it appears only as a visibly optional, separate report item, not as an acceptance check.
- **Open items:** the executor's model is unknown, so I added no model-specific tuning. I did no live retrieval. `guidance.md` is a synthetic snapshot dated 2026-10-10, and the Claude Code notes are cached from 2026-10-12, so neither counts as live-verified.
- **Review:** I did one self-review pass, comparing the final clauses against your original request in both directions. This is not an independent verification.