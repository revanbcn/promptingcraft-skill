I fixed the retry bug and added tests for it, but I couldn't run the tests or open a draft MR. Bash was denied in this session, so none of the three "done when" points is verified by a run.

**Root cause:** `retry_jobs` in `worker.py` is the only retry code in the repo. It built a retry entry for every job from its `retry_delay` and never looked at `status`, so `failed_final` jobs were retried too.

**Fix:** `retry_jobs` now skips jobs whose `status == 'failed_final'`. For every other job it returns the same `{'job_id': job['job_id'], 'delay': job['retry_delay']}` as before. A job with no `status` key is still retried. The job ID is copied through unchanged, and there are no new dependencies and no schema changes.

**Tests:** `tests/test_worker.py` is new; the `tests/` directory was empty. It has two cases:
- A lone `failed_final` job produces no retries.
- A mix of `failed`, `failed_final`, `pending` and no-status jobs returns only the non-final ones. Their IDs and delays match the input exactly (5, 30 and 1).

**Not run:** I never ran the tests: the README's command is `python3 -m unittest discover -s tests -v`, and I would have added `-t .` so `worker` imports. Please run it yourself. I also didn't confirm that the new test fails on the old code, though by reading it the `failed_final` case should.

**Draft MR:** The host has no MR tools and no commit or push was made, so there is no link. Suggested description:
- **Title:** Stop retrying `failed_final` jobs
- **Body:** `retry_jobs` ignored job status and re-queued terminal jobs. It now skips `failed_final` and leaves other statuses' delays and job IDs unchanged. Tests are in `tests/test_worker.py`.

I did not merge or deploy anything.

**Monitoring gaps (not implemented):**
- Nothing counts or logs jobs skipped because they are `failed_final`.
- Nothing alerts when a job reaches `failed_final`.
- Jobs with no `status` key are silently treated as retryable.