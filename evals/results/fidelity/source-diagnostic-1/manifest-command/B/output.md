I composed the handoff below without executing it. I didn't read `manifest.json` or run any commands.

```text
Task: In manifest.json, repair the verify command so it runs the existing local unittest suite.

Context
- manifest.json is in the working directory. Its verify command is currently broken. Find out why before you change it.
- The local unittest suite already exists. Run that suite; don't add a new one.

Constraints
- Add no new dependencies.
- Preserve this immutable policy exactly, byte for byte, with the same field order and values:
  {"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}
- Preserve the build command and the dependency map.
- Do not add product behavior.

Authority
- Local edits and running tests are authorized.
- Commits and deployment are not authorized.

Done when
- The verify command in manifest.json runs the existing unittest suite, and you have run it to confirm that.
- The policy, the build command and the dependency map are unchanged.
- In your final report, give the old and new verify command and the test output you saw. Say so if you could not run something.
```

**Notes**
- **Requirements kept:**
  - **Task and constraints:** the verify repair, no new dependencies, no product behavior, and preserving the build command and dependency map.
  - **Policy:** the immutable policy is copied verbatim.
  - **Authority:** local edits and tests are allowed, and commits and deployment are not.
  - **No additions:** I didn't add a ban on other actions, a file freeze, a particular test command, or an instruction about planning.
- **Unknowns:** I don't know the current verify command, how the suite is laid out, or the manifest's format. The prompt leaves the executor to find these out.
- **Executor and model:** the executor is Claude Code, per your request. The model isn't established, so I applied no model-specific tuning.
- **Guidance freshness:** I had no usable fresh official retrieval. I used the skill's offline Claude Code notes, which are dated cached notes (summary checked 2026-10-12), and `guidance.md`, which is a synthetic fixture from 2026-10-10. Neither is current official guidance, and I'm not claiming it is.
- **Checks:** I compared the final prompt with your original in both directions and made one self-review pass. That is self-review only, not independent verification.