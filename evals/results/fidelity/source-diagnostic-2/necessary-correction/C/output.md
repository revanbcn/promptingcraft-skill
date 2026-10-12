**Review result: a material revision is needed.** The original prompt contradicts itself on authority. It says "deployment is forbidden" and also "After the tests pass, deploy immediately." An executor could read the second sentence as overriding the first. Nothing in the prompt says which one wins.

**Decision for you:** Is deployment forbidden, as the authority sentence says, or do you want it after the tests pass? Until you answer, the handoff below treats deployment as forbidden. That is the narrower reading and the one tied to the stated owner authority. It does not add any new ban on commits, publishing or other steps.

```text
Fix settings.py so save_settings returns 500 without showing success on status 500. Preserve the API.

Authority: Owner authority covers local edits and tests only. Deployment is forbidden.

Run the relevant tests to check the fix. Verifying that save_settings does not show success when the status is 500 tests the requested bug.

Open authority conflict: the original request also said "After the tests pass, deploy immediately." That conflicts with "deployment is forbidden" and has not been resolved. Do not deploy. Hold the deployment step until the owner explicitly authorizes it. Finish the local edit and tests, then report the results and note that deployment is held.
```

**Notes**
- **Coverage:** The fix, "Preserve the API", the local edits and tests authority, and the deployment prohibition all survive with their original strength.
- **Authority:** Nothing new is granted. The "deploy immediately" instruction is preserved as an unresolved conflict, not as a mandate. Only the deployment step is held. The edit and tests proceed.
- **Unchanged:** I didn't invent a root cause, file paths, test commands or edge cases. The executor will find these itself.
- **Freshness:** `guidance.md` is a supplied summary of the Claude Code best-practices page, externally verified 2026-10-12. It has no publication date. I did not retrieve it myself and have no live retrieval. It supports giving the executor context, precise constraints and a way to check the result. It does not supply any authority to deploy. The skill's Claude Code notes are cached offline guidance, last checked 2026-10-12.
- **Limits:** This was a single self-review pass, not independent verification. It does not show that the fix will work downstream.