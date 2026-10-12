The original handoff has one material defect. It asks for "deploy it", but the confirmed authority stops at release preparation. I kept the rest of the task and changed only that span. I left out phase approvals and any ban on other stages.

```text
Prepare a release for this project and get it ready to deploy. Then deploy it only once the owner has separately approved production deployment.

Authority:
- The owner has confirmed authority for investigation, edits, tests and release preparation. Work through these without asking for approval at each phase.
- Production deployment is not covered. It needs a separate owner approval, and nothing so far counts as that approval.
- Until that approval exists, do not deploy. If a step such as a merge or tag would trigger a deploy automatically, hold that step and keep going with the other preparation.

Context:
- The deployment CLI and the project's release process are unknown to me. Find them in the repository, such as its docs, scripts and CI config, and use what you find.
- If more than one release target or process looks equally plausible, ask which one is meant. Don't pick one yourself.

Outcome:
- The release is prepared and verified, with test results or other observable evidence rather than an assertion that it works.
- Report what you prepared and what you checked. Give the exact deploy command or step that is waiting on owner approval, and say plainly that deployment has not happened.
```

- **Changed:** "and deploy it" is now conditional on a separate owner approval, matching the authority you described. The prompt also says that an automatic deploy trigger must not fire before that approval.
- **Added context:** the unknown deployment CLI is treated as something the executor discovers in the repo. An ambiguous release target is a question to you, not a guess.
- **Left open:** the target model is not assumed, so the prompt has no model-specific tuning. Commits, tags and pushes aren't banned, since you didn't ban them.
- **Source freshness:** guidance came from dated offline notes and the synthetic `guidance.md` fixture (snapshot 2026-10-10). Nothing was live-verified, and the handoff doesn't depend on `guidance.md`.