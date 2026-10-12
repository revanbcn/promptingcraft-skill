# Trigger eval 1 — 2026-10-12

Codex CLI 0.162.1, model `gpt-6.1-sol`, installed `promptcraft@dondego-local` 0.2.0.
Queries: `evals/trigger/queries.json`. Runner: `scripts/evaluate_triggers.py` (3 runs per
query, triggered only when the installed `SKILL.md` was read). `runs.json` lists all 65
attempts: 60 valid runs and 5 host-side failures, which are excluded (three transport
failures re-run as `run: "retry"`, two capacity responses retried by the runner). `summary.json` has per-query
rates. Result: train 12/12, validation 8/8; positive runs 30/30 triggered, negative runs
0/30. Raw event traces are not committed because they contain local paths.
