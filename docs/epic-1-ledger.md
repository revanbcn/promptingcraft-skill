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
