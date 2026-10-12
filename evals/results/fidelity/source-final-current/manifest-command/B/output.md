Here is the handoff. I only composed it and did not run the task.

```
In manifest.json, repair the verify command so it runs the existing local unittest suite. No new dependencies.

Preserve this immutable policy exactly: {"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}
Preserve the build command and dependency map.

Local edits and tests are authorized; commits and deployment are not. Do not add product behavior.

To check the result, run the repaired verify command and confirm it executes the existing unittest suite. Then confirm the policy, build command and dependency map are unchanged.
```

- **Scope:** The task wording is kept as given. The only additions are the two closing check sentences, which restate your "preserve" requirements as a check.
- **Not added:** I added no ban on commits beyond what you stated, and no file freeze beyond "preserve". The policy text is copied character for character.
- **Unknowns:** The executor has to find the test location and the current verify command itself. I didn't assume either.
- **Target and freshness:** I took the target to be Claude Code, per your request, with the model unestablished. The guidance in `guidance.md` is synthetic context dated 2026-10-10, and no live official retrieval was available. I'm not claiming it is current. The handoff doesn't mention it.