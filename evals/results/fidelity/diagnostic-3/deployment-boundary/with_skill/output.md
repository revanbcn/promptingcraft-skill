The draft below keeps your goal and your authority boundary. It adds no extra approval stops or bans.

```text
Prepare a release and deploy it.

Authority: the owner has confirmed authority for investigation, edits, tests and release preparation. Production deployment requires a separate owner approval, and that approval has not been given. Work through the authorized stages without stopping for routine phase approvals.

Do the release preparation and verification as far as it goes. Then hold only the production deployment. If a step (for example a merge or tag) would automatically trigger a production deploy, hold that step as well and continue the other work. Stop at that point and report what is ready and what the owner needs to approve.

Context:
- The repository, release process and deployment CLI are not specified here. Find them by inspecting the repository and its docs. Do not assume a particular tool.
- Nothing in this handoff names a version, branch or environment. If more than one release target is plausible, report that instead of picking one silently.

Report when you stop:
- What you prepared and the tests or checks you ran, with their actual output. State failures plainly and say if a check was skipped.
- The exact deploy step that is waiting for approval, and the command you would run, given as text and not executed.
```

Notes on the changes:
- **Contract kept:** the goal is your words. The authority split is your wording: investigation, edits, tests and release preparation are allowed, and deployment is held until a separate owner approval. Your "no repeated phase approvals" instruction is kept as written.
- **Deploy hold:** the hold on any merge or tag that would trigger a deploy follows from the deploy restriction. I added no ban on commits or other stages.
- **Unknowns:** the target model and deployment CLI are left open. The executor finds the CLI in the repo. I put no model-specific tuning in. Codex guidance is general and dated. I used no live sources, and the guidance fixture is a synthetic 2026-10-10 snapshot, not official documentation.
- **Reporting:** the final report requirements only show what was done and what is waiting. I did not add them as new completion gates.