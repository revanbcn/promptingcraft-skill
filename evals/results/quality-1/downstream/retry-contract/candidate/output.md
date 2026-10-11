`retry_jobs` no longer retries jobs with status `failed_final`. Both new tests pass, but I could not open a draft MR, so there's no link.

**Root cause:** `retry_jobs` in `worker.py` never looked at `status`. It turned every job into a retry entry with `{'job_id', 'delay': retry_delay}`, so terminal jobs were retried too.

**Fix:** `retry_jobs` now skips jobs whose `status` is `failed_final`. For every other job it builds the same `{'job_id': job['job_id'], 'delay': job['retry_delay']}` entry as before. A job with no `status` key is still retried. The change is in `worker.py`, and the schema and dependencies are untouched.

**What I ran:** `python3 -m unittest discover -s tests -v`, the command from the README. The repo had no `tests/` directory, so I added `tests/test_worker.py` with two tests.
- **`failed_final` job:** it produces no retry entry.
- **Other statuses:** `failed`, `pending` and a job with no status keep their delays (30, 60 and 5). Their job IDs `a`, `c` and `d` come out unchanged. A `failed_final` job mixed into the same list is dropped.

**Not verified:** I checked the unchanged schedule and job IDs only against the expected values written in the new tests. I didn't run the old code against them.

**Draft MR:** the host has no MR tools, and nothing is committed. The description below is ready to paste.

> **Title:** Stop retrying jobs in `failed_final` status
>
> `retry_jobs` ignored job status and retried every job. It now skips jobs whose status is `failed_final`. Delays and job IDs for all other jobs are unchanged. Added `tests/test_worker.py` covering both cases.
>
> I have not merged or deployed this.

**Monitoring gaps (not implemented):** nothing counts or logs the jobs skipped as `failed_final`. There is also no alert for jobs sitting in `failed_final`, and no signal for jobs that were wrongly retried before this fix.