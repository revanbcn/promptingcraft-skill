# With/without comparison 1 — 2026-10-12

Generation: Codex CLI 0.162.1, model `gpt-6.1-sol`, reasoning `xhigh`, installed
`promptcraft@dondego-local` 0.2.0, one operator. `cases.json` holds five synthetic
single-turn requests with contracts. Each ran twice with the plugin enabled and twice
disabled (`-c plugins.promptcraft@dondego-local.enabled=false`) in a fresh empty directory
(no repository) with a read-only sandbox; `scripts/evaluate_ab.py` reproduces the procedure.
`runs.json` records each run: `SKILL.md` was read in 10/10 enabled runs and 0/10 disabled runs.
`outputs/` holds the final answers (one local path redacted).

Grading: one blinded pass by a separate model (Claude Sonnet 5.5) over the 20 outputs
under seeded shuffled labels; see `grader-prompt.md`. `grades.json` is the grader's answer
with per-item verdicts and reasons, `blind-key.json` maps labels to conditions, and
`results.json` joins them.

Raw: with 6/10 pass, 5 defects; without 3/10 pass, 18 defects. Contract item 3 of
`ab-review-scope` conflicted with the user's "without changing its scope" and failed all
four runs of that case; after inspection it and the matching "mandates refactor, upgrade
and blog post" defect were excluded (`cases.json` `contract_note`). Adjusted: with 8/10
pass, 3 defects; without 3/10 pass, 16 defects. The exclusion was decided after the
grades were seen.

This is prompt fidelity from one generating model, one grader and one operator on five
synthetic requests, not downstream task success and not a statistically powered test.
