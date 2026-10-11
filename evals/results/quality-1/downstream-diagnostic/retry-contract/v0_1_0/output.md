I made the fix and added tests, but I couldn't run anything. The Bash tool was denied partway through, so no test results exist.

**Root cause (from reading the code, not from reproducing it)**
`retry_jobs` in `worker.py` returned a retry entry for every job it received. It never looked at `status`, so `failed_final` jobs were rescheduled with their `retry_delay`.

**Files changed**
- `worker.py`: `retry_jobs` now skips jobs where `job.get('status') == 'failed_final'`. The `job_id` and `delay` of every other job are built exactly as before. No IDs are regenerated and no jobs are created. A job with no `status` key is still retried.
- `tests/test_worker.py` (new, stdlib `unittest`):
  - `failed_final` job is not retried.
  - Other statuses, and jobs with no status, keep their `retry_delay` unchanged.
  - Job IDs are preserved: for `a`, `b` (`failed_final`) and `c`, the result is `['a', 'c']`.

**Test commands and results**
- None were run.
- The command from the README is `python3 -m unittest discover -s tests -v`, run from the repo root.
- The repo had no tests before, so there was no existing suite to run.

**Not verified**
- Acceptance item 1: I didn't see the new test fail before the fix and pass after it.
- Acceptance items 2 and 3: I didn't see any test output for them.
- Acceptance item 4: no existing suite was found or run.
- The fixture has no explicit attempt limits or backoff logic, so I couldn't check those beyond the `delay` pass-through.
- Draft MR: not created. The host has no MR tools, and Bash was unavailable. There is no link.
- Nothing is committed. The changes are only in the working tree, and `__pycache__/` was already untracked.

To finish, run the README command from the repo root. To see the pre-fix failure, run `git stash push worker.py` first, then `git stash pop`. If you restore Bash access, I can do that and report the output.

**Suggestions (not implemented)**
- Log or count skipped `failed_final` jobs.
- Alert if a `failed_final` job ever reaches the worker, since it indicates an upstream filter gap.