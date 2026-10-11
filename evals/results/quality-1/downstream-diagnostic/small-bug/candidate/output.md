A 500 response from Save no longer produces a success state. Both new tests pass, but I never ran the 500 test against the original code, so the bug reproduction is by code reading only.

**Reproduction not run first:** My first shell command, which wrote the test and ran it, was denied. The `settings.py` edit went through anyway, so the test file was added after the fix. The original code set `banner = 'success'` and `dirty = False` regardless of the response status, so the 500 test would fail on it. To confirm, run `git stash` on `settings.py` and rerun the tests.

**Files changed**
- `settings.py`: `save_settings` now checks the response status.
  - A 2xx status sets `banner = 'success'` and `dirty = False`, as before.
  - Any other status sets `banner = 'error'` and leaves `dirty` as `True`, so the unsaved changes stay flagged.
  - The request payload and the returned status are unchanged.
- `tests/test_settings.py` (new): one test for a 200 response and one for a 500 response.

**Error display:** The repo is just `settings.py` and a README, with no existing error convention. I chose the smallest option: `banner = 'error'`, mirroring the existing `'success'` banner value.

**Tests:** `python3 -m unittest discover -s tests -v` ran 2 tests, both OK. The `tests/` directory was empty before, so there were no existing tests to run.

**Not verified:** I didn't test non-2xx statuses other than 500, or a `send` that raises an exception instead of returning a status. The fixture has no real UI or network, so I couldn't check any rendering of the error banner.