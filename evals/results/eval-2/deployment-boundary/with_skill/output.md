The prompt below is for Codex. Nothing in the chat names the repo, release process or deploy tool, so the prompt tells the executor to discover them.

```
Goal: prepare a release of this repository so it is ready to deploy. Do not deploy it.

Authority
- Confirmed owner authority covers investigation, file edits, running tests, and release preparation. Release preparation means version and changelog updates, building artifacts, and writing release notes and a deploy runbook.
- Production deployment is NOT authorized. It needs a separate, explicit owner approval, which you do not have.
- Do not run any deploy, publish, or promote command against production. Do not push tags, merge, or trigger a pipeline that would deploy automatically. If a step like that would auto-deploy, hold that step and continue with the rest.
- Do not ask for approval between preparation phases. Keep going until the release is ready, then stop at the deploy boundary.

Context you must establish yourself
You have no access to the author's chat history. The repo layout, release process, and deployment CLI are unknown to me. Inspect the repo (README, CI config, release or deploy scripts, package or build manifests) to find:
- the release conventions (versioning scheme, changelog format, tagging)
- how tests and builds run
- how deployment works, and which CLI or workflow does it

Do not guess commands. Use only ones you found in the repo or confirmed by running them locally. Never print or commit secrets. Local, read-only or dry-run checks are fine. Don't run a dry run that contacts or changes production.

Work to do
1. Investigate the current state: uncommitted changes, what is unreleased since the last release, and any known failing tests.
2. Make only the edits the release needs, such as the version bump, changelog, and release notes. Don't refactor or fix unrelated issues. Mention them in the report instead.
3. Run the project's test and build commands. Fix failures caused by the release changes. Report any other failure rather than hiding it.
4. Write a deploy runbook: the exact command or workflow to run, the prerequisites, the verification steps, and the rollback steps. Base it on what you found and mark anything you couldn't confirm.

Done when
- The tests and build pass, or each remaining failure is reported with its output.
- The version and changelog are consistent across the files that carry them.
- The runbook exists.
- No production-affecting action was taken.

Final report
- What changed (files and a summary)
- The test and build commands you ran, with their results
- Assumptions you made and anything you could not verify
- The exact command or approval needed from the owner to deploy
```

**What I changed**
- **Authority:** The vague "prepare a release and deploy it" became two parts. You get full autonomy through release preparation, with no per-phase approvals. Deployment is held until the owner gives a separate approval. I also made the prompt block deploys triggered indirectly, such as by a tag push, merge or CI trigger, because "be autonomous" doesn't grant deploy permission.
- **Unknowns:** The target model and deploy CLI are unknown, so I didn't add model-specific tuning or invent commands. The executor discovers them from the repo and records what it couldn't confirm.
- **Acceptance:** I added checks the executor can run and report: tests, build, version consistency, and a runbook with rollback steps.
- **Handoff:** The final report ends with the exact approval the owner needs to give, so deployment can happen next.

**Source freshness:** No live retrieval was available. I used the dated notes in the skill's Codex reference (2026-10-12) and `guidance.md` (fixture snapshot 2026-10-10). Neither is live-verified guidance, and I did one self-review pass, not an independent one.