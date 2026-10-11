`save_settings` now shows success only on a 2xx response. A 500, or a request that raises, now gives an error banner and keeps the user's edits.

**Root cause:** `save_settings` in `settings.py` never looked at the response status. It set `banner = 'success'` and `dirty = False` right after `send()` returned, so a 500 looked like a success. A request that raised was never caught, so it blew up with no error banner. The cause is on the client; the server contract is untouched.

**Files changed**
- `settings.py`:
  - A status outside 200–299 sets `banner = 'error'`, leaves `dirty` as it was, and returns the status as before.
  - An exception from `send` sets `banner = 'error'` and returns `None`.
  - Success behavior is unchanged.
- `tests/test_settings.py` (new): three tests, for a 200 response, a 500 response and a raised `ConnectionError`.

**Tests**
- The repo had no tests, so I added `tests/` with plain `unittest`, which is the only tooling in the README.
- Before the fix, with the command `python3 -m unittest discover -s tests -v`, the 500 test failed (`'success' != 'error'`) and the rejected-request test errored with an uncaught `ConnectionError`. The 200 test passed.
- After the fix, the same command ran 3 tests, all OK.
- Lint and type check: the repo has no lint or type-check configuration, and I was only permitted to run the README command, so I ran neither.

**Assumptions**
- The fixture has no error UI, so I used `form['banner'] = 'error'` as the closest equivalent to the existing `'success'` banner.
- I treat 200–299 as success.
- A rejected request returns `None` instead of a status, because there is no status to return.
- I catch broad `Exception` because the fixture doesn't define a specific network error type.

**Not verified:** the real UI and API client, which aren't in this fixture.