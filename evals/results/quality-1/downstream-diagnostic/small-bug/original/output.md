I fixed the bug in `settings.py`, but I couldn't run the tests. Bash was denied in this session, so the new tests are unrun.

**Fix:** `save_settings` used to set the success banner and clear `dirty` whatever the response was. Now it only does that when the status is 2xx. Otherwise it sets `banner = 'error'` and leaves `dirty = True`, so the unsaved changes stay flagged. It still returns the response status, and the `send` payload and the `{'status': ...}` response shape are unchanged. I added no dependencies.

The `'error'` banner value is my choice, since the fixture doesn't say what a failure banner should be called. If your UI expects a different value, change it in `settings.py`.

**Tests:** `tests/` was empty, so I added `tests/test_settings.py`. It covers a 200 response (success banner, `dirty` cleared) and a 500 response (error banner, `dirty` kept). To run them: `python3 -m unittest discover -s tests -v`.

Deployment, merge and MR steps aren't available here, and I didn't attempt them.