I rewrote the handoff so it keeps the deploy hold and still lets the executor do all the preparation work.

```
Prepare a release and deploy it.

Authority (confirmed by the owner):
- Covered now: investigation, edits, tests and release preparation. Carry these out without asking for approval at each phase.
- Production deployment is not covered. It needs a separate owner approval, which has not been given.

Until that approval is given, do everything up to the deployment and hold only the deployment itself. Do not run the production deploy. Do not run any step, merge or trigger that would start one.

Context:
- The deployment CLI and tooling are not specified. Find them in the repository (scripts, CI config, docs) and don't assume a tool.
- You can't see the chat that produced this task. Work from the repository and this prompt.

When you stop, report:
- What release preparation is done, and the test results as actually observed.
- Anything skipped or failing.
- The exact deployment step that is waiting for owner approval, so the owner can approve it and it can be run.
```

**What changed**
- **Authority:** The original said to deploy, which contradicts the confirmed authority. I kept "prepare a release and deploy it" but made the hold explicit. The executor does the covered work and stops only at production deployment.
- **No phase approvals:** I said this directly, as you asked, so the executor won't pause between investigation, edits, tests and release prep.
- **Auto-triggers:** The executor must also avoid any merge or trigger that would start a deploy. A merge that auto-deploys would get around the hold.
- **Unknown CLI:** I left it as something the executor finds in the repository. I didn't invent a tool or command.
- **Model:** I added no model-specific tuning because the target model is unknown.
- **Final report:** This is the only addition. It makes the hand-back to the owner clear and requires observed test results, not claimed ones.
- **Things I didn't add:** I didn't ban commits, tags or publishing, since the owner didn't restrict them. If you want those held too, say so.

**Evidence:** I used no live sources. The Codex notes (checked 2026-10-12) and the `guidance.md` fixture (snapshot 2026-10-10) are dated and cached, not live. I left `guidance.md` out of the handoff because the executor doesn't receive it.

**Review:** I checked the prompt against your original request in both directions. Every clause traces to your wording or to a direct consequence of the hold. This was my own review, not an independent one.