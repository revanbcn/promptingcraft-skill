# EPIC 1 delivery ledger

Scope: a public prompt-authoring foundation, not an executor or hosted service.
Canonical: GitLab; GitHub: explicit branch/tag mirror; GitLab CI is authoritative.

1. Verify contracts and owner namespaces; preserve an empty owner workspace.
2. Implement the standalone skill, original references and portable packaging.
3. Test freshness against synthetic fixtures before implementing its logic.
4. Run three clean paired behavior cases using existing subscription access;
   separate model behavior, manual observations and deterministic checks.
5. Review all new content independently; resolve material findings.
6. Publish a minimal bootstrap, then reviewed GitLab MR; merge only on green CI.
7. Publish verified archives and v0.1.0; verify public readbacks and mirror parity.

Shared interfaces: skill references must stay inside its standalone package;
registry feeds both skill source routing and freshness utility; archive builder
feeds installation tests and release assets. No provider text is redistributed.

Decisions: standard MIT; Python 3.11+ stdlib maintenance; no mandatory MCP,
API keys, hooks, telemetry, or GitHub Actions. Portable Agent Plugins 1.0.0 root
manifest plus a Claude Code compatibility manifest, one skill tree.

Preflight completed 2026-10-12: empty non-Git directory; authenticated personal
GitLab/GitHub namespaces; preferred slug absent on both; docs MCP search/read
worked. Isolated publication checkout avoids protected owner `.git` location.
KFA helper unavailable; fail open, no retry or publication.

Implementation/verification completed locally: standalone references; portable
and Claude manifests; source registry; freshness/hash/index utility; reproducible
archives; isolated no-overwrite installer. Twenty-one offline tests pass; strict
Claude validation and the live-fetched Agent Plugins JSON schema pass.
Live check fetched usable content from 14/14 configured pages; a second check
reported all unchanged. Private source bodies/model traces were not committed.

Behavior: two three-case paired Claude iterations, two targeted reruns (14 calls),
plus one Codex read/use smoke. Model/authority facts are recorded in eval results;
small-fix assumption drift remains an observed limitation. ChatGPT UI inventory
attempt timed out; native ordinary-chat installation/runtime remains NOT RUN.

Independent review: separate agent, same operator; fixed HTTPException isolation,
index truncation and plugin archive broken links; affected review passed all 21
checks. Follow-up semantic review found assumption drift; recorded without rewriting
historical outputs or claiming clean behavior. No downstream execution benchmark.

Publication: original bootstrap committed; new public repos created in verified
owner namespaces. GitHub Actions disabled; SSH GitLab unavailable, existing
keyring credential used via an ephemeral HTTPS helper (never logged or committed).
Daily schedule ID 4486529 exists with active=false; included compute allowance
and owner recurring quota policy are not established, so activation is held.

Publication checks: GitLab MR !1 required pipeline 2936650464 passed. GitHub
authenticated metadata is public, but unauthenticated page/API/raw readbacks return
404; mirror public access remains blocked/unverified. No credentials or platform
control changes will be used to evade that boundary.
