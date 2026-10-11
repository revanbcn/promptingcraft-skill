Here is the handoff prompt. It is for a Claude Code executor whose model is unknown.

```
Task: add CSV export to the existing report view in this repository.

Context
- You have no access to the discussion that led to this task. Work from the repository itself. Find the report view, the way it chooses its columns, and its ordering logic.
- The repository's own docs and conventions (README, CONTRIBUTING, CLAUDE.md, CI config, release docs) are the authority for build, test, lint, branch, commit and MR rules. Read them before editing.

Desired behavior
- The report view gets an export action that downloads the data as CSV.
- The export must match what the user currently sees: the same selected columns, in the same column order, with the same row ordering. Reuse the view's existing column-selection and sorting state or logic. Do not build a second source of truth.
- CSV formatting must be correct (follow RFC 4180 conventions) for:
  - fields containing commas
  - fields containing double quotes (escape each as "")
  - fields containing newlines (CR, LF or CRLF)
  - empty and null values
  - an empty result set: the file must still be valid and contain the header row for the selected columns. If the view currently disables or hides actions on empty results, follow that convention and state which you chose.
- Follow the project's existing conventions for download mechanics, file naming, labels, i18n and accessibility. If the repository already has a CSV or escaping utility, reuse it.

Constraints
- No backend or API changes. No new dependencies. Do the work with the code and data already on the client or in the view layer.
- Keep the diff focused on this feature. No unrelated refactors.
- If the repository seems to make this impossible without a backend change or a new dependency (for example, the view only receives a paginated slice), stop and report the finding. Do not work around it.

Authorized actions
- Plan, edit, add tests, run local checks, self-review, fix findings, commit, push a branch, open an MR/PR.
- Merge the MR only after every required CI check is green and the repository's merge rules are met. If a required check fails, fix the cause and re-run. Do not bypass, skip or weaken checks, and do not force-merge.
- Respect the existing release workflow. Do this by following its documented steps for changelog entries, version bumps, labels, branch naming and approvals, and by not circumventing them.
- Deployment is NOT authorized. Do not deploy, publish, tag a release or trigger release or deploy pipelines unless the existing workflow does so automatically as part of merge. If merging would trigger a deploy that you cannot separate from it, stop before merging and report.
- Do not claim you have done anything you have not. If something cannot be done (no remote, no CI, no permissions), say so and stop at the last safe step.

Acceptance checks
- Automated tests cover the following, and they pass:
  - column selection and order are preserved
  - row ordering is preserved
  - a field with a comma
  - a field with a quote
  - a field with a newline
  - empty and null values
  - an empty result set
- The repository's standard lint, type-check, test and build commands pass. Use the commands the repo documents, and name them in your report.
- Reviewed diff: re-read your complete diff critically for correctness, edge cases (for example, header escaping, a leading BOM decision, spreadsheet formula-injection risk for cells starting with = + - @) and scope creep. Fix what you find. For the formula-injection point, follow any existing project convention; otherwise make a conservative choice and document it.
- Required CI is green on the MR before merge.

Final report (concise)
- What changed (files and approach) and any decisions or assumptions you made
- Commands run and their results, including the CI status
- The commit and MR links, and the merge status
- Anything skipped, failing or left for a human. Confirm that no deployment was performed.
```

**Notes**
- **Source freshness:** Network retrieval was unavailable. I used only the synthetic `guidance.md` (dated 2026-10-10) as test context. I did not load the skill's own reference files, and no live official Claude Code guidance was verified. The prompt is therefore agent-general and has no tuning for the unknown model.
- **Assumption:** The prompt assumes the view has the full dataset available. If it only has a paginated slice, the executor is told to stop and report instead of changing the backend.
- **Choices left to the executor:** BOM handling and formula-injection handling. They matter in practice, and the discussion didn't settle them.
- **Authority:** Merge is limited to a green required CI and the repo's rules. Deployment is excluded, and the release workflow must be respected.