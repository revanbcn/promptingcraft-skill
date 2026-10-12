Here is the handoff. I read guidance.md and the PromptCraft contract, Claude Code, and rubric notes. Those notes are dated cached guidance, not live-verified or current. No network retrieval was available, and the executor's model isn't established.

```
In manifest.json, repair the verify command so it runs the existing local unittest suite.

Context:
- The unittest suite already exists in this repo. Find it and how it is normally invoked; do not assume a path or command.
- Whether the verify command is wrong, missing, or broken in some other way is not yet known, so inspect it first.

Constraints:
- Add no new dependencies.
- Preserve this immutable policy exactly, byte for byte: {"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}
- Preserve the build command and the dependency map.
- Do not add product behavior.

Authority:
- Local edits and running tests are authorized.
- Commits and deployment are not authorized.

Done when: the repaired verify command, run from the manifest, executes the existing unittest suite. Report the command you ran and its result. Also confirm that the policy, build command and dependency map are unchanged.
```

Notes on what I did:
- **Immutable policy:** I copied it verbatim.
- **Dependencies:** "No new dependencies" only forbids adding them. It doesn't freeze the rest of manifest.json, so I didn't add a whole-file freeze.
- **Commit and deploy:** I kept both unauthorized, as you stated.
- **Suite location and invocation:** The prompt leaves these for the executor to discover. I didn't invent a specific unittest command.
- **Drift check:** I checked every clause in both directions against your request. I found no added requirements, and nothing was dropped.