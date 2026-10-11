```
Task: add CSV export to the existing report view in this repository.

Context: you can't see the discussion that led to this task. Inspect the repo first (report view, how it picks and orders columns, existing tests, CONTRIBUTING/CI/release docs) and follow its conventions. Don't guess commands. Find the real test, lint and build commands from the repo.

Required behavior
- Users can export what the report view currently shows as a CSV file.
- The export keeps the user's currently selected columns and their current order. Use the view's existing source of truth for both, not a separate copy.
- Fields containing commas, double quotes (escaped by doubling) or newlines must be quoted correctly, so the file round-trips through a standard CSV parser.
- An empty result must export cleanly and must not error.
- Provisional assumption, subordinate to any existing behavior or convention in the repo: an empty result produces a header-only file with the selected columns. If the UI or the repo's conventions say otherwise (for example, disabling the button), follow those and report what you chose.

Constraints
- No backend or API changes and no new dependencies. Build the CSV from data the view already has on the client.
- Keep the change small and in the style of the surrounding code.

Authorized, with no further approval needed: plan, edit, add tests, run checks, review your own diff, fix findings, commit, push a branch, open an MR/PR, and merge it once all required CI checks are green and the repo's merge rules are met.

Not authorized: any deployment, release publication or production change. Respect the existing release workflow. Do not bypass branch protection, required reviews or CI, and don't skip hooks. If merging would automatically trigger a deploy or release, don't merge. Leave the MR ready and report that.

Acceptance (run for real and show the output)
- Tests cover: column selection and order preserved, commas, quotes, newlines, and an empty result, using whatever test framework the repo already has.
- The repo's existing tests, lint and type checks pass.
- You self-reviewed the final diff and fixed any real issues.
- If the export can be exercised in the app, confirm it once. Otherwise say you couldn't.

Final report: files changed, the empty-result decision, the check results, the MR link and CI status, whether you merged (or why you held), and anything you didn't verify.
```

Notes:
- **Empty results:** you only said to handle them. I labeled "header-only file" as a provisional assumption inside the prompt that yields to existing UI behavior, rather than making it a requirement.
- **Merge and deploy:** merging is authorized only after required CI is green. The prompt tells the executor to hold the merge if it would auto-trigger a deploy, because deployment isn't authorized.
- **Commands and model:** I didn't name test, build or CI commands, since I haven't seen the repo. The prompt tells the executor to discover them. It has no model-specific tuning, since the executor model is unknown.
- **Sources:** `guidance.md` and the skill's Claude Code notes are dated offline context (2026-10-10 and 2026-10-12). Nothing was verified live. My one self-review pass found nothing that needed changing.