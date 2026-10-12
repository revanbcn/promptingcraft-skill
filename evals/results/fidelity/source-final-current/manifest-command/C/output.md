The task is clear and the supplied guidance doesn't change it, so this is a minimal handoff built from your words.

```
In manifest.json, repair the verify command so it runs the existing local unittest suite. No new dependencies.

Preserve this immutable policy exactly: {"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}

Preserve the build command and dependency map.

Local edits and tests are authorized; commits and deployment are not. Do not add product behavior.

Check: run the repaired verify command and confirm it executes the existing unittest suite. In your final report, give the command output and confirm the policy, build command and dependency map are unchanged.
```

- **Mode:** Implementation. You authorized local edits and tests, and the handoff keeps that grant and the commit/deploy exclusion as you stated them.
- **Immutable policy:** Copied verbatim.
- **Added check:** The final check only confirms the requested outcome: the verify command runs the existing tests, and the preserved items are unchanged. I added no new behavior or gates.
- **Unspecified details:** I left the unittest invocation, the location of the policy in the manifest, and the planning process open. The executor can find them in the repo.
- **Guidance source:** I used the supplied `guidance.md`, verified externally on 2026-10-12. I did no retrieval of my own. It is reference only and isn't part of the handoff. The Claude Code notes in the skill are cached guidance, not live-verified.
- **Executor model:** Not established, so I applied no model-specific tuning.