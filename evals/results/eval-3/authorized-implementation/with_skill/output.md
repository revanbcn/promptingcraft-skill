Here is the handoff prompt. Evidence status: `guidance.md` is a synthetic fixture dated 2026-10-10, and the Claude Code notes are dated cached guidance. Nothing was verified live.

```text
Task: add CSV export to the existing report view in this repository.

Context: you can't see the chat that produced this task. Inspect the repo first and follow its conventions. Read CLAUDE.md, CONTRIBUTING and the CI/release docs if they exist. Don't assume any of them says more than what you find.

Requirements
- Add an export action to the existing report view that downloads the data as CSV.
- The export must contain the columns currently selected in the view, in the current order. It must not fall back to a default or full column set.
- Escape correctly: fields containing commas, double quotes (doubled) or newlines must stay in one field and parse back to the original values.
- Handle empty results without errors.
- Do not change the backend. Do not add dependencies. Build the CSV client-side from data the view already has.

Provisional assumptions (subordinate to existing behavior and to anything you find in the repo)
- Empty results: export a header-only file. If the view already defines different behavior for empty results, such as a disabled button, follow that and say so.
- Use the encoding and line-ending conventions already in the codebase. Otherwise use RFC 4180-style CSV with UTF-8.
- Don't widen scope with extras such as new formats, filters or settings.

Workflow (authorized): plan briefly, edit, add tests, run the project's own test, lint and build commands, review your diff, fix findings, commit, open an MR, and merge once all required CI checks are green. Respect the existing release workflow, branch rules and review requirements.

Not authorized: any deployment. If merging would trigger a deploy automatically, don't merge. Finish everything else, then report that the merge is on hold. Don't bypass or weaken CI, branch protection or hooks.

Acceptance
- Tests cover: selected columns and order preserved; commas, quotes and newlines; empty results.
- The repo's existing checks pass. Don't invent commands. Find them in the repo.
- If a check can't run, say so. Don't claim it passed.

Final report: files changed, commands run with results, CI status, MR link, merge status (or why it was held), and any assumption you had to rely on.
```

Changes and assumptions:
- **Empty results:** your request didn't say what the file should contain. I made "header-only" a provisional default inside the prompt, and it yields to existing view behavior.
- **Deploy hold:** "merge after CI" doesn't authorize deployment. The prompt tells the executor to hold the merge if it would trigger a deploy automatically.
- **No invented specifics:** the file names, commands and framework are unknown, so the prompt tells the executor to discover them.
- **Model tuning:** the executor model is unknown, so I applied Claude Code-level guidance only and did no model-specific tuning.