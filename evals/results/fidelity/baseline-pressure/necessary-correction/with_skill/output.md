The task needs a revision. It contradicts itself on authority, and that is the only material problem.

- **Conflict:** "Owner authority covers local edits and tests only; deployment is forbidden" conflicts with "After the tests pass, deploy immediately." The authority limit is explicit and scoped, so it decides the conflict. The executor does the fix and runs the tests. It holds the deploy until the owner grants authority, and it doesn't treat "immediately" as permission.
- **Left unchanged:** the fix, "preserve the API", and the test run all stay as you wrote them. I added no mechanism, no new test framework and no edge cases. The file path and test command aren't given, so the executor has to find them.
- **Source freshness:** I used the synthetic `guidance.md` (snapshot 2026-10-10) and the dated Claude Code notes (checked 2026-10-12), both offline. Nothing was live-verified, and the target model isn't established.

```text
Fix settings.py so that save_settings returns 500 and does not show success when the status is 500. Preserve the existing API.

Authority: you may make local edits and run tests only. Deployment is forbidden. The original task also said to deploy right after the tests pass. That request is on hold because it conflicts with the owner's limit, so do not deploy, release, or push anything. Stop once the fix is made and the tests have run. Deployment can happen only after the owner explicitly grants that authority.

Find settings.py and the existing tests in the project and run them. When you finish, report:
- what you changed
- the test command you ran and its actual result (say so plainly if anything fails or can't be run)
- evidence that a status 500 now yields a 500 return with no success shown
- that deployment was not performed and is awaiting owner authorization
```