# EPIC 4 — native plugin integration ledger

Base: MR !3, `dbdf3cd9097e4d61445e3e3d4ef1d01fc9418c77`. Canonical release v0.1.0 unchanged.

- [x] Inspect actual repository, portable/Claude manifests and existing ZIP builder.
- [x] Retrieve current official plugin, skill, ChatGPT use and account/role documentation.
- [x] Inspect existing Codex marketplace/plugin registrations before additive writes.
- [x] Add documented catalog and generated real source, using one maintained skill.
- [x] New marketplace tests RED → GREEN; 90 regressions, schemas, resources and package checks pass.
- [x] Actual supported CLI registration/discovery/install, installed + enabled readback.
- [x] Six native scenarios / seven CLI turns; installed cache reads and actual multi-turn resume.
- [x] Supported ChatGPT Desktop check: app access denied by Computer Use policy; no bypass.
- [x] Exact minimal owner-side installation/Chat verification steps prepared.
- [x] Fresh-context final code/evidence review: no blockers; 0/5 positive outputs with material drift.
- [x] GitLab MR [!4](https://gitlab.com/revanalex/promptcraft-skill/-/merge_requests/4) created.
- [ ] Latest-head required CI, merge and main CI readback — HOLD: GitLab `ci_quota_exceeded`; verify never started.
- [ ] Stable owner-root registration/cache refresh and retention of unrelated sources — safe local delivery continues separately from merge.

Open gate: ChatGPT Desktop installation/ordinary Chat activation/end-to-end behavior
need supported owner UI execution. Codex success does not close this gate. No
release or publication authorization inferred. No downstream advantage claimed.

Developed by the dondego.com team.

Post-commit merge, CI and stable-root delivery receipts are recorded in MR !4;
these preparation checkboxes do not predict actions that have not yet occurred.

CI hold observed on MR head `179fb329a53d6c8d3a76e330213b876523855dcd`:
[pipeline 2937994791](https://gitlab.com/revanalex/promptcraft-skill/-/pipelines/2937994791),
required verify job `17106555572`, `failure_reason=ci_quota_exceeded`, runner absent,
no start time. Project runner inventory contains no active eligible runner and
current-user runner inventory is empty. No quota purchase, runner credential
creation, local-only replacement of required CI, or merge-gate weakening occurs.
Merge remains held until required CI can actually run and pass.
