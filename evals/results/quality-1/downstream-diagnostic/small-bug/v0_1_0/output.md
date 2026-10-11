Save now shows success only on a 2xx response. A 500 or a failed request shows an error and leaves the form's edits and dirty state alone. I couldn't run lint or a type check.

**Root cause:** `save_settings` in `settings.py` set `banner = 'success'` and `dirty = False` right after calling `send(...)`. It never looked at `response['status']`, and it had no handling for `send` raising. This is a client-side bug, so I didn't touch the request or response format.

**Fix:** In `settings.py`, `send` is now wrapped in `try/except`.
- **Exception:** the banner is set to `'error'` and the function returns `None`.
- **Non-2xx status:** the banner is set to `'error'` and the status is returned.
- **2xx:** unchanged. The banner is `'success'`, `dirty` is `False`, and the status is returned.

**Files changed:**
- `settings.py`
- `tests/test_settings.py` (new)

**Test evidence:**
- **Command:** `python3 -m unittest discover -s tests -v`, the command from the README.
- **Before the fix:** the 500 test failed (`'success' != 'error'`) and the network-failure test errored (`ConnectionError` propagated). The 2xx test passed.
- **After the fix:** all 3 tests pass.
- **What the tests cover:** a 500 and a raised `ConnectionError` each leave the banner at `'error'`, `dirty` true and the values intact. A 200 still gives the success banner and a clean form.

**Could not verify:**
- **Lint and type check:** I tried `python3 -m ruff check .` and `python3 -m mypy settings.py`, but the sandbox denied the call. The repo has no lint or type-check config. I also didn't run `py_compile` or the other checks I'd bundled into the first compound command, which was also denied. The unittest run did import and exercise `settings.py`.
- **Existing tests:** `tests/` was empty, so there were no existing tests to run.

**Assumptions:**
- **Error treatment:** the fixture has no existing error treatment, so I used `form['banner'] = 'error'` to mirror the `'success'` banner.
- **Status check:** I treat a 2xx status as success, the equivalent of `response.ok`.
- **Exception handling:** I catch any `Exception` from `send` as the network or rejected-request case.