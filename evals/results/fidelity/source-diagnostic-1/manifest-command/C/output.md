I wrote the handoff without running or editing anything. Per the PromptCraft checks, the policy is copied verbatim, and nothing in it goes beyond your contract.

```text
In manifest.json, repair the verify command so it runs the existing local unittest suite.

Constraints:
- No new dependencies.
- Preserve this immutable policy exactly: {"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}
- Preserve the build command and the dependency map.
- Do not add product behavior.

Authority:
- Local edits and tests are authorized.
- Commits and deployment are not authorized.

Context: I don't know the project's layout or how the verify command is currently broken. Find that out from the repo, including where the existing unittest suite lives and how it is normally invoked.

To check the result, run the repaired verify command locally and confirm it runs the existing unittest suite. In your final report, include what you changed and the command output, and say which parts of manifest.json (policy, build command, dependency map) you left untouched.
```

**Notes**
- **Contract coverage:** Every requirement and exclusion from your request is in the prompt with its original strength. I added no commit or publish bans of my own. Commits and deployment are simply not granted.
- **"No new dependencies":** I did not freeze manifest.json or any other file. Only the policy, build command and dependency map are required to stay as they are.
- **Planning:** The prompt neither requires nor forbids planning. The break in the verify command is unknown, so the executor decides how much exploration it needs.
- **Verification step:** Running the repaired command only checks the requested outcome. I added no coverage targets or extra gates.
- **Evidence:** The guidance I used on how to write a Claude Code handoff is the guidance.md you supplied, which you say was externally verified on 2026-10-12. I did not retrieve it myself and had no live retrieval. I also read PromptCraft's own cached Claude Code notes, which are dated the same day, so I treated them as cached, not live.
- **Unestablished:** The executor's model is unknown, so I applied no model-specific tuning. Nothing here shows the handoff will succeed downstream.