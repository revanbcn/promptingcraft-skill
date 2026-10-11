Here's the task prompt. It's based on guidance.md, a synthetic fixture dated 2026-10-10. I couldn't check any official sources.

---

**Task: Add CSV export to the existing report view**

You're working in a repository you haven't seen before, and you can't see the discussion that led to this task. Everything you need is below. Check the repo's actual state before acting on any assumption here.

**Goal**
Add a CSV export to the existing report view. A user viewing a report can download exactly what they see as a CSV file.

**Required behavior**
- The export contains the report's currently selected columns, in their current order. Reuse the view's existing column-selection and ordering state. Don't create a second source of truth.
- Header row: use the same column labels the view shows, unless the codebase has a clear convention for something else.
- CSV escaping follows RFC 4180:
  - Fields containing commas, double quotes, or newlines (`\n` or `\r\n`) are wrapped in double quotes.
  - Embedded double quotes are doubled.
  - Newlines inside a field are preserved within the quoted field.
- Empty result set: export a valid CSV with the header row only. It must not crash, download a zero-byte file, or silently do nothing. If the existing UI has a convention for disabling actions on empty data, follow it and say which you chose.
- Null and undefined values become empty fields. Don't output the strings "null" or "undefined".

**Constraints**
- No backend or API changes. Build the export from data the view already has on the client.
- No new dependencies. Don't edit the manifest or lockfile except where the repo's own workflow requires it, and say so if that happens.
- Match the surrounding code's style, naming, comment density, and test framework. Keep the diff small and focused.
- Don't refactor unrelated code.

**Authorized**
Plan, edit, write and run tests, review your own diff, fix issues, commit, open an MR/PR, and merge it once the required CI checks are green.

**Not authorized**
- Deployment or release publishing of any kind.
- Bypassing, skipping, or weakening CI, hooks, branch protection, or required reviews.
- Merging with failing or pending required checks.

Follow the repo's existing release workflow (CONTRIBUTING, CI config, changelog or versioning conventions, branch naming, commit message format). Only make release-related changes the workflow requires of a contributor, such as a changelog entry. Don't trigger the release itself.

**Process**
1. Explore: find the report view, how columns and ordering are stored, how downloads or other exports are done (if any), the test setup, and the contribution and release docs. Briefly state your plan before editing.
2. Implement.
3. Tests, at minimum:
   - Selected columns and their order are preserved, including after the user reorders or hides columns.
   - Fields with commas, quotes, and newlines are escaped correctly.
   - An empty result gives header-only output.
   - Null and undefined values give empty fields.
   Put the CSV-building logic in a pure function so it can be tested without the DOM.
4. Run the project's tests, linter, type checker, and build. Report the exact commands and results.
5. Review your own diff against the requirements above. Fix any problems and re-run the checks.
6. Commit, push a branch, and open the MR. The description should cover the behavior, the testing, and any judgment calls.
7. Wait for the required CI checks. Merge only if they are all green and the repo's merge rules are met. If CI fails, fix and re-push. Don't merge around a failure.

**Stop and report instead of guessing if**
- The directory isn't a git repository, there's no remote, or you can't create an MR with the available tooling or credentials.
- The report view can't produce the export without a backend change or a new dependency.
- The selected-column or ordering state is ambiguous, for example if the server decides ordering.
- Required CI is red for reasons unrelated to your change, or the merge needs approvals you don't have.

**Final report**
Include:
- What changed, listed by file.
- Test and CI results. State plainly what passed, failed, or was skipped.
- The MR link and its merge status.
- Confirmation that nothing was deployed.
- Any assumptions you made.

---

**Notes on how I wrote it**
- I wrote the prompt so it doesn't depend on the executor model. It spells out checks and stop conditions instead of relying on a model's judgment.
- The environment I'm in isn't a git repository, so I added a stop condition for that. Your real target repo may differ.
- I treated the merge as authorized only because you said so explicitly. It's conditioned on green required CI, and deployment is excluded.