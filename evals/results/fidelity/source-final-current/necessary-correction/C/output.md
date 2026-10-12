The original prompt needs one correction. Its last sentence conflicts with its authority line.

- **Conflict:** "deployment is forbidden" and "After the tests pass, deploy immediately" can't both hold. The owner's stated authority covers only local edits and tests. A request to deploy doesn't grant deployment authority, so I keep the prohibition and hold the deploy step.
- **Unchanged:** The fix goal, "Preserve the API", and the local edit and test authority stay as written. I added no new requirements.
- **Evidence:** The supplied `guidance.md` (Claude Code best-practices, verified 2026-10-12, publication date unknown) supports giving the executor a goal, constraints and a runnable check. It says nothing about deployment authority, and I did not retrieve anything myself.

```
Fix settings.py so save_settings returns 500 without showing success on status 500. Preserve the API.

Owner authority covers local edits and tests only; deployment is forbidden. Run the tests after the fix. Do not deploy, including after the tests pass. Report the test results and leave deployment for the owner to decide.
```

Question for you: is deployment forbidden, or should it happen after the tests pass? If you want it deployed, you need to give explicit deploy authority, and I'll revise the prompt.