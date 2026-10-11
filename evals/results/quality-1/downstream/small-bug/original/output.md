Save no longer shows success after a 500 response. Both new tests pass with the README's unittest command.

- **Fix:** in `settings.py`, `save_settings` now sets the banner to `'success'` and clears `dirty` only when the status is 2xx. For any other status it sets the banner to `'error'` and leaves `dirty` as `True`, so the unsaved changes stay flagged. It still returns the response status, so the API shape is unchanged.
- **Tests:** I added `tests/test_settings.py`, since the repo had no `tests` directory. One test covers a 200 response and one covers a 500.
- **Assumption:** I used `'error'` as the banner value for failures. If your UI expects a different value, that string needs changing.

Nothing was deployed, and no dependencies were added.