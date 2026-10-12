The original prompt is already suitable. No material revision is necessary.

```
Fix settings.py so save_settings returns 500 without showing success when the API returns status 500. Preserve the request payload and the status-200 success behavior. No new dependencies. Local edits and tests are authorized; do not commit or deploy. Verify both 500 and 200 behavior using the existing tests and report actual results.
```

**Review findings**
- **Goal:** The prompt names the file, the function, the failing case (API status 500) and the required result (return 500, no success shown).
- **Constraints:** It keeps the request payload and the status-200 success behavior unchanged. It also forbids new dependencies, and it doesn't freeze manifests or lockfiles.
- **Authority:** It grants local edits and tests and forbids committing and deploying. I added no grants or bans.
- **Verification:** It asks for the existing tests to check both the 500 and 200 paths and for actual results to be reported. That checks the requested behavior without adding completion gates.
- **Open choices:** The prompt doesn't say how to implement the fix or whether to plan first, and I left both open. It names one file, so there is no ambiguity about the target.

**Freshness:** I read `guidance.md`, which is a synthetic fixture dated 2026-10-10, and treated it as dated test context only. No live official retrieval was available, so I'm not claiming current guidance. The executor won't see `guidance.md`, and the prompt doesn't depend on it.