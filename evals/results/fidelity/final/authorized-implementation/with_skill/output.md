The request is prompt authoring, so I composed the handoff and did not run the task. The target is Claude Code, and the model is unknown, so I used agent-level guidance only. No live retrieval was available. The guidance is dated cached notes from 2026-10-12 plus the synthetic guidance.md fixture dated 2026-10-10, not live-verified official sources.

```
Add CSV export to the existing report view.

Requirements
- The export preserves the report's current selected columns and their ordering.
- It correctly handles values containing commas, quotes and newlines.
- It handles empty results.
- No backend change and no new dependencies.

Context
- The report view, its column-selection state and any existing export or download patterns are not described here. Find them in the repository.
- The expected output for an empty result (for example, header row or no header) was not specified. Follow any convention already in the codebase. If there is none, choose the least surprising behavior and state it in your summary.

Authorized
- Plan, edit, add and run tests, review your own diff, fix issues, commit, open an MR, and merge it once the required CI checks are green.
- Respect the repository's existing release workflow.

Not authorized
- Deployment. If merging would trigger a deployment, hold the merge, finish everything else, and report that it is waiting for authorization.

Verification
- Run the relevant existing tests and add tests for the requested behavior: column selection and order, commas, quotes, newlines, and empty results.
- In your final summary, report the commands you ran and their results, the MR link, the CI status, and whether the merge happened or is being held.
```

- **Scope:** The prompt keeps the conversation's own words and constraints. It adds no mechanism, file path or test framework.
- **Empty results:** You didn't specify the output format, so I left it open. It follows codebase convention, with the choice disclosed if none exists. I did not choose a header-only file.
- **Merge and deploy:** Merge is authorized after green CI, and deployment is not. I made the merge conditional on the release workflow not auto-deploying. I added no other bans on commit, MR or merge.
- **Planning:** I left planning to the executor, as you authorized it. The prompt does not say to skip it.
- **Executor environment:** I did not assume the executor sees this chat, CLAUDE.md or guidance.md, so the prompt is self-contained.