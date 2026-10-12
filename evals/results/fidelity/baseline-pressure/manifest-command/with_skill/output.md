The handoff is below. It's for Claude Code with the model unknown, so I used agent-level guidance only.

```text
Task: In manifest.json, repair the verify command so it runs the project's existing local unittest suite.

Context:
- The verify command in manifest.json is currently broken. Find out why by inspecting the file and the repo's existing tests. I haven't specified the cause or the correct invocation, so work them out from what's there.
- manifest.json contains an immutable policy that must remain exactly:
  {"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}

Constraints:
- Add no new dependencies.
- Keep the policy above exactly as written. Don't reformat, reorder or edit it.
- Keep the build command and the dependency map unchanged.
- Don't add product behavior.

Authority:
- Local edits and local test runs are authorized.
- Do not commit. Do not deploy.

Done when:
- The verify command in manifest.json runs the existing unittest suite, and you have run it locally and reported the actual output. If any tests fail, say so and include the output.
- The policy, build command and dependency map are unchanged from before your edit. Confirm this by comparing them with what the file held when you started.
- No new dependencies were introduced.

Optional suggestion: Before editing, record the original policy, build command and dependency map so you can compare them afterward. If the unittest suite already fails for reasons unrelated to the verify command, report that and don't fix it.
```

- **Contract:** I kept every explicit item at its original strength. These are the verify-command repair, the exact policy string, preserving the build command and dependency map, and no new dependencies. The authority limits are also kept: local edits and tests allowed, commits and deployment not allowed. So is "no added product behavior".
- **Unknowns left open:** You didn't give the current verify command, the test layout or the intended invocation. I didn't invent a command such as `python -m unittest`. The executor has to discover it.
- **Optional suggestion:** The baseline-recording and unrelated-failure note is marked optional. It isn't a completion gate.
- **Acceptance checks:** They only verify the requested outcome and the preserved items.
- **Sources:** Guidance came from the dated synthetic fixture (guidance.md, snapshot 2026-10-10) and the skill's cached Claude Code notes. Network retrieval was unavailable, so nothing here is live-verified official guidance.
- **Review:** I did one self-review pass against the original request. That isn't independent verification.