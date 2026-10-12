# With/without comparison 1 — 2026-10-12

`cases.json`: five single-turn requests with contracts. Each ran twice with the plugin
enabled and twice disabled (`-c plugins.promptcraft@dondego-local.enabled=false`).
`outputs/` holds the final answers (one local path redacted). A fresh grader saw them
under shuffled labels; `blind-key.json` maps labels to conditions and `results.json`
holds the grades (raw and adjusted for the contract item noted in `cases.json`).
Adjusted: with 8/10 pass, 3 defects; without 3/10 pass, 16 defects. This is prompt
fidelity from one model and one operator, not downstream task success.
