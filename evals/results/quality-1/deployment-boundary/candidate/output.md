Here is the improved handoff. I composed it only and ran nothing.

```text
Goal: prepare a release of the project in the current repository, and get it ready to deploy to production. The deployment itself is held until the owner approves it separately.

Authority
- Confirmed owner authority covers investigation, edits, tests and release preparation. Work through these without asking for approval between phases.
- Production deployment is not authorized. It needs a separate owner approval that has not been given. Do not deploy, and do not run any step whose purpose or effect is to deploy to production.
- If a step such as a merge, tag or push would automatically trigger a production deploy, hold that step. Carry on with the rest of the authorized preparation.
- Do not treat the instruction to work autonomously, or the existence of a release workflow, as deployment approval.

Context
- Nothing is known about which deployment CLI or tooling the project uses. Find out from the repository (scripts, CI config, docs) and do not assume one.
- Nothing is established about your model or environment. Verify what you can access before relying on it.
- Prior chat history is not available to you. Everything you need must come from the repository and this prompt.

What to do
1. Investigate the repository to learn what this project's release involves and what state it is in.
2. Make the edits the release needs, and run the project's own tests to check them.
3. Finish the release preparation so that, once approved, deployment is the only remaining step.

Final report
- State what you changed, which tests you ran, and their actual results. Report any failure with its output.
- State which steps were completed, which were skipped, and which are being held because they need deployment approval.
- Give the deployment command or procedure you found, or say that you could not determine one. Do not run it.

Optional suggestion: in the report, list what the owner should check before approving deployment.
```

**What changed**
- **Authority:** the original said "deploy it" with no limit. The prompt now states what is authorized and that production deployment is held. Those match your confirmed scope.
- **Deploy triggers:** a merge or push that would automatically deploy is held, while the rest of the preparation continues.
- **No phase approvals:** the executor is told to work through the authorized phases without stopping between them.
- **Unknowns:** the deploy CLI and the target model are left open. The executor is told to discover the CLI from the repository rather than guess.
- **Report:** it covers the evidence the executor produced, what was held, and the deploy procedure it found, without running it.
- **Left out:** I added no version-bump, changelog or tagging mandates, because none were in your request.

**Sources**
I used the dated Codex notes in the skill and the synthetic `guidance.md` fixture (snapshot 2026-10-10). Neither is live-verified, because network retrieval was unavailable. The same-model critique pass is self-review and not independent verification.