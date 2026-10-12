**Finding:** The task needs a material revision. The original contradicts itself on authority. It says "Owner authority covers local edits and tests only; deployment is forbidden." It then says "After the tests pass, deploy immediately." Passed as written, the executor could deploy without authority, or it could stall.

The bug fix and the local tests are clear and authorized. I held back only the deployment step. Deployment stays blocked until the owner explicitly grants it, and I added no other prohibitions or gates.

**Deciding question for you:** Do you want deployment authorized, which means removing "deployment is forbidden", or kept forbidden, which means dropping the "deploy immediately" step? Until you answer, the handoff below blocks deployment.

```
Fix settings.py so save_settings returns 500 without showing success on status 500. Preserve the API.

Owner authority covers local edits and tests only; deployment is forbidden.

The original request also said "After the tests pass, deploy immediately." That conflicts with the authority above and is not authorized, so do not deploy. When the tests pass, stop and report the results. Deployment awaits explicit owner authorization.

Verify with the project's tests, and report the actual test results.
```

**Notes:**
- **Provenance:** Your original wording is kept for the fix, "Preserve the API", and the authority limits. The last line only asks the executor to run tests and report the results, which is what "After the tests pass" already implies.
- **Evidence:** The Claude Code guidance in `guidance.md` was supplied and verified externally on 2026-10-12. I did not retrieve it myself. It supports giving a check the executor can run, and it doesn't grant any authority. The skill's offline Claude Code notes are cached guidance, not live-verified.
- **Unknowns:** I don't know which model or environment the executor has, or what the test command is, so I left discovery to the executor. I did not run or execute the task.