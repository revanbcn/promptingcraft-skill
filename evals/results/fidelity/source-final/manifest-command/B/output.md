Here is the handoff. I only composed it and did not run the task.

```
In manifest.json, repair the verify command so it runs the existing local unittest suite. No new dependencies.

Preserve this immutable policy exactly: {"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}
Preserve the build command and dependency map.

Do not add product behavior.

Authority: local edits and tests are authorized. Commits and deployment are not authorized.

Check: run the repaired verify command locally and confirm it executes the existing unittest suite. In your final report, include the command output and say which files you changed.
```

**Notes**
- **Preserved:** The task wording is kept as given. The policy JSON is copied character for character. The authority split is unchanged: local edits and tests are allowed, and commits and deployment are not.
- **Added:** The only addition is the check, which runs the repaired command. It verifies the requested outcome and sets no new completion bar. The "report the output and changed files" line asks for evidence of that run.
- **Left open:** I didn't invent the exact command, the test directory or the runner syntax. The executor can discover them from the repo. I also didn't freeze other files or manifest fields, because the task only requires that the build command, dependency map and policy stay unchanged.
- **Left out:** `guidance.md` is not mentioned in the handoff, since it is authoring context and not task input.
- **Guidance freshness:** `guidance.md` is a synthetic fixture dated 2026-10-10. The Claude Code notes are cached offline notes, summarized 2026-10-12. No live official retrieval was available, so I'm not claiming this follows current guidance. The target model is unestablished, so I used only agent-level guidance and no model-specific tuning.