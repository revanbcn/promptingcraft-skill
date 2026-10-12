Here is the handoff. I didn't inspect any code, so it leaves file locations and the exact symptom for the executor to find.

```text
Repair the worker that retries jobs after a terminal failure.

Context
- "Terminal" means status equals failed_final. The worker currently retries jobs after such a failure, and that is the behavior to repair.
- You have no chat history. The repository layout and the worker's location are unknown to me, so discover them in the repo. If more than one worker plausibly matches, say so and ask which one is meant before editing.
- The exact failure symptom has not been given. Reproduce or confirm it from the code and any existing tests before changing anything.

Requirements
- Jobs with status failed_final must not be retried after a terminal failure.
- Preserve job IDs.
- Preserve the existing retry schedule for every other status.
- Do not add dependencies.
- Do not change the database schema.

Authority
- Authorized: edits, running local tests, and opening a draft MR.
- Not authorized: merging and deploying. Stop at the draft MR.

Verification
- Run the relevant local tests. Add or adjust a test only where it directly shows that a failed_final job is no longer retried and that other statuses keep their schedule and job IDs.
- In your final report, state which checks you ran and their results. Say plainly if any check could not be run or failed.

Optional suggestion: if you notice monitoring improvements, such as alerting on failed_final jobs, list them separately in your report. They are not part of this fix, so do not implement them.
```

- **Mode:** the request says to repair the worker and authorizes edits, so the prompt is an implementation handoff. It does not add routine approval stops.
- **Unresolved:** I treated "repair" as "stop retrying failed_final jobs" because that follows from the wording. The actual symptom and the worker's location are unknown, so the prompt tells the executor to confirm both and ask if the target is ambiguous.
- **Authority:** the prompt carries over your grants and exclusions unchanged. I didn't add bans on other steps, such as pushing the branch for the draft MR.
- **Monitoring:** this is an optional report item only. It isn't an acceptance gate.
- **Guidance:** I used the dated offline notes (`guidance.md`, snapshot 2026-10-10, and the skill's Claude Code notes). Nothing was live-verified. The executor's model is unknown, so I applied no model-specific tuning.