Here is the handoff prompt.

```
Task: add CSV export to the existing report view in this repository.

Context
- You have no access to the discussion that produced this task. Everything you need is below. Discover the repo's structure, conventions, test setup and CI config yourself. Read CLAUDE.md or equivalent contributor docs if present.
- First locate the report view and how it picks and orders its columns.

Outcome
A user can export the report as a CSV file from the existing report view.

Requirements
- The export has the same columns the report currently shows (the user's selection) and the same order. Rows follow the view's current ordering.
- It is valid CSV. Fields containing commas, double quotes (escaped by doubling) or newlines are quoted correctly.
- An empty result still exports a file with the header row only, and the UI does not error.
- Frontend/client-side only: no backend or API change and no new dependencies. Use what the repo already has.
- Match the surrounding code's style, naming and UI patterns.

Non-goals
- No new export formats, no column-picker changes, no unrelated refactors.

Authorization
- Authorized: plan, edit, add tests, run local checks, self-review and fix findings, commit, push a branch, open an MR/PR, and merge it after all required CI checks are green.
- Not authorized: any deployment, release publishing or production change. Respect the repo's existing release workflow and branch/merge rules, and don't bypass or weaken checks, protections or required reviews.
- Before merging, check what merging triggers. If it would automatically deploy or release, do not merge. Leave the MR green and ready, and report that it is held. Do the same if a required approval or check is missing, pending or failing and you can't legitimately fix it.
- Do not use admin overrides or skip hooks.

Acceptance (run what the repo provides and report the real output)
- Tests cover: column selection and order preserved, comma/quote/newline escaping, empty result, and a normal multi-row case.
- The repo's existing test, lint and type/build checks pass locally. Don't invent commands. Find them in the repo's config.
- If feasible, check the export in the running UI. If you can't, say so.

Process
- Plan briefly before editing. If the report view's data flow is unclear, explore first.
- After implementing, review your own diff for correctness and scope creep, and fix what you find.

Final report
- Summarize the changes and list the files touched.
- Give the checks you ran with their results, and say what was skipped or couldn't be verified.
- Give the MR link and its CI status.
- State whether it was merged. If not, say why.
- State explicitly that nothing was deployed.
```

**Notes**
- **Target:** I treated this as Claude Code, since you said so. The model is unknown, so I used no model-specific tuning. The prompt doesn't assume the executor has this chat or CLAUDE.md.
- **Evidence:** Guidance came from the dated synthetic `guidance.md` (snapshot 2026-10-10) and the offline Claude Code notes. Nothing was live-verified, because retrieval was unavailable.
- **Merge:** Merging after green CI is authorized as you specified. Because deployment isn't, I added a hold: if the merge would auto-trigger a deploy, the executor stops short of merging and reports back. I did not treat "autonomous" as permission for either.
- **Assumptions:** I assumed the export is client-side and that the repo has existing test and CI commands. I left the commands unnamed and had the executor find them.
- **Drift check:** The final prompt keeps every constraint you gave and adds no new approvals.