The handoff is below. I composed it only and did not run or inspect the task.

```
In manifest.json, repair the verify command so it runs the existing local unittest suite. No new dependencies.

Preserve this immutable policy exactly: {"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}

Preserve the build command and dependency map.

Do not add product behavior.

Authority: local edits and tests are authorized. Commits and deployment are not authorized.

Check your work by running the repaired verify command locally and confirming it runs the existing unittest suite.
```

**Notes**
- **Contract:** Every clause comes from your wording. The policy JSON is copied verbatim, in the same order. "No new dependencies" is kept as written and doesn't freeze other files.
- **Discovery:** I didn't name a specific unittest invocation or test path. I haven't seen the repo, so the executor finds them.
- **Final check:** This only confirms the requested outcome. I added no coverage or other completion gates.
- **Provenance:** I left `guidance.md` out of the handoff because it is authoring reference. It is a supplied summary of the Claude Code best-practices page, verified externally on 2026-10-12. I have no live retrieval and did not fetch the page myself. The summary says nothing about the executor's model, so I applied no model-specific tuning.
- **Review:** I did one self-review pass against your original text and found no omissions, added requirements or authority changes. That is not independent verification.