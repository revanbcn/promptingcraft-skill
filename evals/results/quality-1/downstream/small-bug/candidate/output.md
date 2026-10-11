A 500 response from Save no longer shows a success state. I reproduced the bug first, then fixed it, and both tests now pass.

**Files changed**
- `settings.py`: the fix.
- `tests/test_settings.py`: new. The repo had no tests.

**Cause:** `save_settings` set `banner = 'success'` and `dirty = False` after calling `send`, without looking at the response status.

**Fix:** The success banner and `dirty = False` are now set only for 2xx statuses. Any other status sets `banner = 'error'` and leaves `dirty = True`, so the unsaved changes stay flagged. The function still returns the status, and the request and response shapes are unchanged.

**My choice on the error state:** The repo has no error-display convention, so I picked the smallest option: `banner = 'error'`. I treated every non-2xx status as a failure, not only 500. I don't know whether the real UI renders an `'error'` banner.

**Test results** (`python3 -m unittest discover -s tests -v`):
- Before the fix, `test_500_does_not_show_success` failed with `AssertionError: 'success' == 'success'`, which reproduces the bug.
- After the fix, both tests pass (`Ran 2 tests ... OK`): the 500 case and a 200 control case.

**Not verified:** There is no real UI or API in this fixture, so I tested only with a stubbed `send` that returns status 500. Nothing was committed, pushed, or deployed.