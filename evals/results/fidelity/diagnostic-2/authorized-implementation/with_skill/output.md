```
Add CSV export to the existing report view.

Requirements
- Export preserves the report's currently selected columns and their ordering.
- Handle commas, quotes, newlines and empty results correctly. The user did not choose what an empty-result export should contain, so pick a sensible behavior that fits the existing code and state your choice in the final report.
- No backend change.
- No new dependencies.

Authorized, within this task
- Planning, edits, tests, review of your own diff and fixes to what the review finds.
- Commit, opening an MR, and merging that MR once the required CI checks are green.

Not authorized
- Deployment.
- Respect the repo's existing release workflow. If merging would trigger a deployment, hold the merge, finish the rest, and report that the merge is waiting for explicit approval.

Context
- You can't see the discussion this task came from. Find the report view and its existing conventions in the repo.
- Find the repo's own test, lint and build commands, and run the ones relevant to this change.

Verification
- Add or update tests showing that the export keeps the selected columns and their order, that commas, quotes and newlines are escaped correctly, and that an empty result behaves as you decided.
- Run the relevant checks and show the results.

Final report
- What changed.
- Which checks you ran, and their results.
- The empty-result behavior you chose.
- The MR link and its CI and merge status. If the merge is held, say why.
```

Notes:
- **Empty results:** your wording ("handle empty results") doesn't say whether the file should be header-only, completely empty, or blocked with a message. I left that open and asked the executor to report its choice. If you have a preference, add it.
- **Executor model:** it's unknown, so I used general Claude Code guidance with no model-specific tuning.
- **Sources:** I couldn't retrieve anything live. The guidance is dated cached notes plus the synthetic `guidance.md` fixture (2026-10-10). It isn't live-verified official documentation.
- **Release workflow:** I made the merge conditional on it not triggering an unapproved deploy. Your grant covers merging after green CI, and the prompt keeps that grant without letting a deploy through.
- **Planning:** I didn't dictate a planning approach, since you authorized planning without prescribing how.