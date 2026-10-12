I composed the handoff below and did not run any of the release work.

```
Prepare a release for this project and, once the owner separately approves it, deploy it.

Authority (confirmed by the owner):
- Covered now: investigation, edits, tests and release preparation. Carry these out end to end without asking for approval at each phase.
- Not covered: production deployment. It needs a separate owner approval, and nothing in this task supplies it. Continuing autonomously, a release workflow or an automatic trigger does not grant it.
- If an action, such as a merge or a tag, would automatically trigger a production deploy, hold that action and keep going with the other preparation work.

Context:
- You are starting without this chat's history. Find the project layout, release process, version scheme and deployment tooling in the repository and its docs.
- The deployment CLI is not specified. Identify it from the repository. If it is ambiguous, or if more than one release or deploy target is equally plausible, ask the owner which one rather than choosing.
- The target model is unknown, so don't rely on model-specific behavior.

Outcome:
1. Release preparation: bring the project to a state that is ready to release. Run the project's own tests and release checks, and fix what you find within the scope of getting this release ready.
2. Deployment: once the release is prepared, stop before deploying. Report what is ready to ship, which deployment command and target you would use, and the evidence from the checks. Ask the owner for approval to deploy to production.
3. Deploy only after the owner gives that approval, and only the release you prepared.

Report:
- What you changed.
- Which checks you ran, with their actual results. Say plainly if any failed or were skipped.
- What is still held, and why.
```

**What changed and why**
- **Authority is explicit.** The original said "deploy it" but granted only preparation. The handoff separates the two, stops before production, and makes the deploy a distinct approval step. It also holds any merge or tag that would trigger a deploy automatically.
- **No routine phase approvals.** The executor does preparation, tests and fixes in one run.
- **Unknowns stay open.** The deployment CLI and the target model are not guessed. The executor discovers the CLI from the repository and asks if it is ambiguous. I added no bans on commits or publishing, because you didn't state any.
- **Fresh-agent context.** The prompt tells the executor it can't see this chat and must find the project details itself.
- **Reporting.** The report requires real check results, and failures or skipped steps must be stated.

**Drift check:** every operative clause traces to your request. The only additions are the discovery instructions and the report, which only serve verification.

**Source freshness:** `guidance.md` is a synthetic fixture dated 2026-10-10. It is dated context only, not live-verified official guidance. The Codex notes are cached from 2026-10-12. Network retrieval was unavailable, so I did no live revalidation.