`retry_jobs` no longer retries `failed_final` jobs, and both new tests pass. I couldn't open a draft MR here, so there's no MR link.

**Root cause**
- `retry_jobs` in `worker.py` built a retry entry (`job_id` plus `delay` from `retry_delay`) for every job. It never looked at `status`, so `failed_final` jobs were rescheduled like any other.
- I reproduced this before changing anything: the new test failed with `[{'job_id': 'a', 'delay': 30}] != []`.

**Files changed**
- `worker.py:5`: the list comprehension now skips jobs where `job.get('status') != 'failed_final'` is false. Delay and ID handling are untouched.
- `tests/test_worker.py` (new): the repo had no tests directory, so I created one with two tests.

**Test command and results**
- I ran `python3 -m unittest discover -s tests -v`.
- Before the fix, both tests failed.
- After the fix, both tests pass (`Ran 2 tests ... OK`).

**Acceptance**
1. `test_failed_final_is_not_retried` fails before the fix and passes after it.
2. `test_other_statuses_keep_schedule_and_ids` shows `failed` and `pending` jobs keep their `retry_delay` values (30 and 120).
3. The same test checks that job IDs `a` and `c` come through unchanged. The worker only copies IDs, and no jobs are created.
4. There was no existing suite, so "the existing suite passes" can't be shown. Only the two tests I added ran.

**Could not verify**
- **Draft MR:** the fixture has no MR tooling, so I didn't open one and haven't committed anything. `__pycache__/` is still untracked.
- **Backoff and attempt limits:** the fixture has no backoff or attempt-limit logic, only the per-job `retry_delay`. I could only confirm that value passes through unchanged.
- **Missing `status` key:** I used `.get('status')`, so a job without that key is still retried, as before.

**Suggestions**
- Log or count jobs skipped for being `failed_final`.
- Add a test covering jobs with no `status` key.