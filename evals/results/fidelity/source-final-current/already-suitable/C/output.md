The original prompt is already suitable. No material revision is necessary.

```
Fix settings.py so save_settings returns 500 without showing success when the API returns status 500. Preserve the request payload and the status-200 success behavior. No new dependencies. Local edits and tests are authorized; do not commit or deploy. Verify both 500 and 200 behavior using the existing tests and report actual results.
```

**Contract check**
- **Goal:** `save_settings` returns 500 and shows no success when the API returns 500. The prompt states this as the task, so the executor should reproduce the failure rather than treat it as missing information.
- **Invariants:** the request payload and the status-200 success behavior stay unchanged. Both are unconditional, and I added no exceptions.
- **Constraint:** no new dependencies. It doesn't freeze manifests or lockfiles, and I didn't add that.
- **Authority:** local edits and tests are authorized. Commit and deploy are forbidden. I added no other grants or bans.
- **Check:** verify the 500 and 200 paths with the existing tests and report actual results. That is feasible and directly tests the requested behavior. It doesn't require new test frameworks or coverage targets.
- **Process:** the prompt neither forces nor forbids planning. For a small, clear fix, Claude Code can go straight to the change or explore first. That fits the supplied guidance.

**Not specified:** which file or function `settings.py` and `save_settings` refer to, and which tests count as the existing ones. Discovery can settle both. If several plausible `settings.py` files exist, the executor should ask rather than pick one.

**Evidence and freshness**
- The Claude Code best-practices guidance in `guidance.md` was externally verified on 2026-10-12, according to the supplied file.
- I did no live retrieval myself.
- The guidance only supports giving the executor context, constraints and a runnable check. It sets no model-specific rules and doesn't show that the prompt will succeed.
- I did not execute the task.