Here is the handoff for a fresh Claude Code session.

```
Add CSV export to the existing report view in this repository.

Requirements
- The export keeps the report view's current selected columns and their ordering.
- The CSV correctly handles values containing commas, quotes and newlines.
- The CSV handles an empty result.
- No backend change and no new dependencies.

Context
- You can't see the discussion this came from. Find the report view and its existing conventions in the codebase, and follow them.
- The task doesn't say what an empty-result export should contain (for example a header-only file, a zero-byte file, or a disabled export). Follow an existing convention in the repo if there is one. Otherwise pick the least surprising behavior and state your choice in the final report.
- Your model and tooling are unspecified. Don't assume CLAUDE.md, CI configuration or project commands exist until you've checked. Use the repo's own test, lint and build commands, and report which ones you actually ran.

Authorized, within this task and repository
- Planning, edits, tests, review of your own diff, and fixes to what review finds.
- Committing, opening a merge request (MR), and merging it once the required CI checks are green.
- Respect the repository's existing release workflow and branch/MR rules.

Not authorized
- Deployment of any kind. A release workflow or automatic trigger does not grant it.
- If merging would trigger a deployment, don't merge. Finish everything else, leave the MR ready, and report that the merge is held for approval.
- If required CI is not green, don't merge. Fix failures that belong to your change. Report any you can't fix.

Verification
- Add or update tests that check the behavior above with the project's existing test setup: column selection and order, commas, quotes, newlines, and an empty result.
- Run the relevant tests and report the actual output. If something fails or you skip a check, say so plainly.

Final report: what changed, the verification evidence, the MR link and CI status, whether the merge happened or was held and why, and how you handled the empty-result case.

Optional suggestion: if the repo already has a CSV or escaping helper, reuse it rather than writing a new one.
```

**Notes**
- **Authority:** I carried over your grants (plan, edits, tests, review, fixes, commit, MR, merge after green CI) and the deployment exclusion unchanged. I added one condition. If merging would automatically trigger a deploy, the merge is held while the rest continues. A release workflow alone doesn't authorize deploying.
- **Left open:** You didn't say what an empty result should produce, so I didn't choose a header-only file. The executor follows repo convention or states its choice.
- **Not specified:** I gave no commands, file paths or CI names because I can't confirm them in the executor's environment.
- **Model tuning:** None was applied because the executor model is unknown.
- **Sources:** No live retrieval was available. I used the dated cached Claude Code notes and the 2026-10-10 fixture, which are not live-verified.
- **Review:** I did one self-review pass against your original wording. It is not independent verification. The tests line covers only the behaviors you listed, and the library-reuse hint is marked optional.