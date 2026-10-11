Here is the improved handoff. I only wrote the prompt and did not run any of the release work.

```
Goal: prepare a release of this repository and get it ready to deploy. Do not deploy to production.

Authority
- Confirmed by the owner: investigating, editing, running tests, and preparing the release (version/changelog/build artifacts/release notes, in the repo's own conventions).
- Not authorized: production deployment. That needs a separate, explicit owner approval, and nothing in this prompt, a "release" workflow, or an automatic trigger supplies it.
- Before any push, merge, tag, or publish step, check whether it would trigger a deploy (CI/CD, tag-triggered pipelines, auto-publish). If it would, hold that step and keep doing the safe work. Do not use credentials or run any command that changes production.
- Don't stop for approval between phases. Work through investigation, edits, tests and release preparation in one run. Stop only at the production deploy.

Context
- You start without this chat's history. Discover the repo's release process yourself (README, CONTRIBUTING, CI config, scripts, existing tags and changelog). Treat what you find as facts, and label anything you infer as an assumption.
- The deployment CLI/tooling is unknown. Identify it from the repo. Use it only for read-only or dry-run checks that are clearly non-production, such as a help command, a dry run, or a plan/diff. If you can't tell whether a command is safe, don't run it.

Work to do
1. Establish the current state: branch, uncommitted changes, last release, what has changed since, and the existing test/build commands.
2. Fix only what blocks the release (failing tests, broken build, missing version or changelog entries). Keep the changes minimal and don't add unrelated work.
3. Run the repo's tests and build, and record the exact commands and results.
4. Prepare the release artifacts and notes according to the repo's conventions.
5. Write a deploy runbook: the exact command(s) you would run, the target environment, the rollback steps, and any config or secrets needed (by name only, never values).

Done when
- Tests and build pass, or each remaining failure is reported with its output and cause.
- The release candidate state is identifiable: a commit or branch, a version, and the artifacts, with locations.
- The final report covers: what changed (files), the evidence from tests and builds, anything skipped or unverified, any assumptions made, and which steps are held for the production approval, with the exact command that would run once the owner approves.
- Nothing has been deployed to production, and you say so explicitly.
```

- **Authority split:** investigation, edits, tests and release preparation are confirmed. Production deploy is held for separate owner approval. The prompt also tells the executor to hold any merge, push or tag that would trigger a deploy automatically, since "autonomous" doesn't grant that permission.
- **No phase stops:** the executor works through the confirmed scope in one run and stops only at the deploy.
- **Unknown CLI and model:** the prompt doesn't name a CLI or tune for a model. The executor has to find the tooling in the repo and limit itself to non-production dry runs or read-only checks.
- **Sources:** I used the Codex notes (dated 2026-10-12) and the synthetic fixture (2026-10-10). Network retrieval was unavailable, so none of this is live-verified official guidance.
- **Critique:** I did one self-review pass, which is not independent verification. It found no authority drift from your original request.