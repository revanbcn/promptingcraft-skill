Used `guidance.md` (synthetic snapshot, 2026-10-10); no live official guidance was verified. Self-review preserved scope and left model, paths, and commands unspecified.

```text
Fix the Save flow so an HTTP 500 response cannot produce a success indication.

Known context: Save currently shows success after HTTP 500. The repository paths, framework, request client, and executor model are unknown. Locate the relevant code and existing test conventions in the provided repository; do not assume access to the prompt author’s files or chat history.

Trace the Save response handling and identify why the failure reaches the success path. Make the smallest focused correction. Preserve the existing API shape, including endpoint, request payload, and response contract. Add no dependencies and avoid unrelated refactoring. Use the existing error-display conventions; if none exist, state your bounded assumption before choosing a minimal failure indication.

Authorization is limited to code/test edits and local verification. Do not commit, push, merge, deploy, or trigger a release.

Acceptance checks:
- A Save request returning HTTP 500 shows failure through the application’s error handling and does not show success.
- A successful Save still shows the expected success indication.
- Regression coverage exercises both outcomes using the repository’s existing test tools. Demonstrate that the 500 check fails before the fix and passes afterward.

Run the affected tests and appropriate existing checks. Review the final diff for API changes, new dependencies, and unrelated edits.

Report the observed cause, changed files, commands run and results, and any verification limitations. Do not claim checks passed if they could not run.
```