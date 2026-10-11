Here's the task prompt. I haven't run or changed anything. Plan mode was on, and the only available tool was Read, so I couldn't write it to the plan file. I used `guidance.md` (a synthetic snapshot dated 2026-10-10, not live official guidance) for structure. It says to state behavior, context, constraints, authority and checks, and that autonomy never implies merge or deploy permission.

---

**Task: Add CSV export to the existing report view**

You have no access to the discussion that led to this task, so everything you need is below. Work in the project repo for the report view. The directory where this prompt was written is not a git repository, so first find the right repo root and confirm it is a git repo with a remote. If you can't, stop and report that.

**Goal**
Users of the existing report view can download the report as a CSV file.

**Required behavior**
- The export contains exactly the columns currently selected in the view, in the current display order. Don't hardcode a column list or use a separate default order.
- Rows follow the view's current ordering. Whether filters apply is not stated, so match what the user currently sees. Check how the view derives its rows and reuse that logic instead of re-deriving it.
- Values are escaped per RFC 4180:
  - Wrap any field containing a comma, double quote, CR or LF in double quotes.
  - Double any embedded quotes.
  - Keep embedded newlines inside the quoted field.
- Empty results produce a valid CSV with the header row only, with no crash and no blank file. If the existing UI has a convention for empty states, follow it. Report which behavior you chose.
- Empty or null cell values export as empty fields.

**Constraints**
- Do not change the backend or any API, and add no new dependencies. Do the work client-side from data the view already has, and write the CSV serialization with the language standard library or existing project utilities. If you think either is truly impossible, stop and report instead of working around it.
- Follow the repo's existing conventions for structure, naming, styling, comments and tests. Reuse existing download, button or utility code where it exists.
- Keep the change minimal. No unrelated refactors.
- Don't print or commit secrets, and don't change CI config to make checks pass.

**Process**
1. **Explore (read-only).** Find the report view, how it holds selected columns, ordering and rows, and the test setup. Read CONTRIBUTING, the README and CI config for the branch, commit, MR and release rules.
2. **Plan.** Write a short plan listing files to touch and how you'll keep column selection and order in sync with the view.
3. **Implement.** Keep the CSV serialization in a small, separately testable function.
4. **Test.** Add tests for the cases below, then run the project's existing test, lint and type-check commands.
   - Plain values.
   - A comma, a quote and a newline, singly and combined.
   - Column subset and reordered columns.
   - Empty results.
   - Empty or null cells.
5. **Review.** Review your own diff against this spec and fix any issues. Confirm that no backend or dependency files, such as lockfiles and manifests, changed.
6. **Deliver.** Commit on a feature branch, push, and open an MR following repo conventions. Wait for the required CI checks to pass, then merge.

**Authority**
- You may plan, edit, test, review, fix, commit, push a feature branch, open an MR, and merge it once all required CI checks are green.
- Respect the existing release workflow. Follow any required steps such as changelog entries, labels, version bumps, review approvals and merge method. Don't bypass branch protection, and don't force-push to the default branch.
- Do **not** deploy or trigger a release or deployment job, manually or otherwise. If merging automatically triggers one under the existing workflow, say so in your report. Don't add steps beyond that.
- If CI fails, fix the cause and re-run. Don't skip, disable or weaken checks. If a required check is blocked or flaky for a reason you can't fix, or review approval is required and missing, stop and report instead of merging.

**Done when (report each with evidence)**
- The export matches the view's selected columns and order, shown by a test.
- Tests pass for commas, quotes, newlines and empty results, with the test output.
- Existing tests, lint and type-check pass.
- The diff has no backend or dependency changes.
- The MR link, the CI status and the merge result are reported. If anything was skipped or failed, say so plainly.

**Report format:** a brief summary of what changed, files touched, test results, MR and CI status, any decisions you made where this spec was silent, and anything left for a human, such as the deployment.

---

Notes for you:
- Because the executor model is unknown, the prompt is explicit and checkable and doesn't rely on model-specific behavior.
- The prompt leaves the filter and empty-state behavior to the executor and asks it to report its choice. If you want those fixed, tell me and I'll add them.
- Merge authority is stated explicitly and conditioned on green CI. Deployment is excluded separately.