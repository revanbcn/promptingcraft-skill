The handoff is below. I didn't run or inspect the task. Evidence for it is the supplied `guidance.md`, which was externally verified on 2026-10-12. I didn't retrieve anything live. The guidance is general Claude Code advice, and nothing in it is tuned to a specific executor model. It also doesn't authorize commits or deployment.

```
In manifest.json, repair the verify command so it runs the existing local unittest suite. No new dependencies.

Preserve this immutable policy exactly: {"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}
Preserve the build command and dependency map.

Do not add product behavior.

Local edits and tests are authorized. Commits and deployment are not authorized.

Discover the repository layout and the existing unittest suite yourself. To check the repair, run the corrected verify command locally and report its actual output, including any failures.
```

Notes:
- **Immutable policy:** I copied it verbatim, with no reformatting.
- **Verification step:** it only runs the repaired command, which directly checks the requested outcome. I added no extra completion gates.
- **Left open:** the exact unittest invocation and the file layout aren't given, so the executor discovers them. If more than one suite or test location looks plausible, it should treat that as a question for you rather than picking one silently.
- **Not added:** I didn't ban other manifest edits, since you only asked to preserve the policy, build command and dependency map.