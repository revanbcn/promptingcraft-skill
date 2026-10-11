I composed the handoff only and did not run the fix. The user gave no file names, field names or commands, so the prompt tells the executor to find them itself and not to assume any.

```
Fix a small input-validation bug in this repository. The details below come from the person who requested the fix. You have no access to the chat where the task was discussed, so confirm anything about the code yourself.

Outcome
- Find the validation that is wrong or missing, and make the smallest change that fixes it. The requester has not given me the exact failing input or the file. Locate them from the code, tests and any bug description in the repo. If you can't identify the intended behavior, ask one focused question before changing anything.

Invariants
- Preserve the API shape. Keep endpoint, function and type signatures, request and response fields, status codes and the error-body format the same. If the fix seems to need a change to any of these, stop and report it.
- Follow the existing validation patterns and error handling already in the codebase.

Non-goals
- No refactors, unrelated cleanups or dependency changes.

Authority
- Edit files locally and run local tests, linters and builds.
- Do not deploy, release, publish or push. Do not merge anything that could trigger a deployment. Stop with the fix ready for review.

Verification
- Add or update a test that fails without the fix and passes with it. Run the project's existing test suite and any type check or lint you can find. Don't invent commands. Check the repo's README, Makefile or package scripts.
- Confirm the API shape is unchanged. For example, check that no public signatures or schemas differ in the diff.

Report
- Say what the bug was, which files changed, and the exact commands you ran with their results. State plainly any check you could not run or that failed, and say that nothing was deployed.

Guidance caveat
- The only prompting guidance available was a cached summary dated 2026-10-10. It is not live-verified. Rely on the repository itself as the source of truth.
```

- **Source freshness:** the only evidence was the synthetic `guidance.md` snapshot (2026-10-10) and the skill's offline Claude Code notes (checked 2026-10-12). Both are dated cached guidance. There was no network access, so nothing is live-verified. The skill's notes describe the cached summary as "2024"; I took the dated fixture as the evidence and did not claim anything about official sources.
- **Executor model:** unknown, so I added no model-specific tuning.
- **Authority:** I kept "do not deploy" explicit and added no approvals. I also held back any merge that could trigger a deploy.
- **Assumption:** I assumed the executor can run local tests. The prompt tells it to find the commands itself.