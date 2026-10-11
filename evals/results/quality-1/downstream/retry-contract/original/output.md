`retry_jobs` in `worker.py` now skips any job whose status is `failed_final`. Both new tests pass with the README's unittest command.

Jobs with any other status, including one with no status field, come back exactly as before. They keep their `job_id` and their `retry_delay` as `delay`, so the existing schedule is unchanged. I added no dependencies and made no schema changes.

There was no `tests/` directory, so I created `tests/test_worker.py` with two cases. One checks that a terminal job isn't retried. The other checks that a mixed list keeps the right IDs and delays for non-terminal jobs.

I did not commit anything or create the draft MR. The host provides no MR tools, so that stage is unavailable here.

Separately, you could log or count the jobs skipped as `failed_final`. That would show whether anything is still enqueuing terminal jobs. It isn't part of this fix.