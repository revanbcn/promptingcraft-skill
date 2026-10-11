```
Task: Reduce the p95 latency of the existing 10,000-row benchmark from about 900 ms to below 300 ms. Keep exact results unchanged.

Context
- You are working in a repository you can inspect. I haven't named the benchmark, the runner, the measurement protocol, or the code under test. Find them in the repo (benchmark scripts, CI config, README, docs) before changing anything.
- Baseline: p95 is about 900 ms. This is the user's figure. Re-measure it yourself and report the number you get.

Requirements
1. Under the same benchmark runner and the same measurement protocol, the 10,000-row benchmark's p95 must be below 300 ms. Don't change the runner, protocol, dataset, row count, iteration or warmup counts, percentile calculation, or thresholds to get the number down.
2. Exact results must be preserved. For identical inputs, outputs must be identical to the pre-change outputs. That includes ordering, values, types, precision, and error and edge-case behavior. Don't use approximations, sampling, lossy caching, or reduced precision.
3. Add no new dependencies. Don't change dependency manifests or lockfiles.
4. Don't deploy, publish, release, or merge. Work only in the local working tree. Don't push or trigger CI or release pipelines.

Approach
- Measure first, with the existing benchmark. Profile to find where the time goes, then fix the dominant costs. Don't guess at them.
- Prefer changes to algorithms, data structures, and avoidable repeated work or I/O. Keep the diff focused and match the surrounding code style.
- Before optimizing, capture reference outputs from the unmodified code. Use the existing tests plus a captured output of the benchmark workload. Compare against them after every change.

Acceptance (report evidence, not assertions)
- Before and after p95 from the same benchmark command and runner, with the exact command used and the full output. If you ran it several times, show the spread.
- Proof of identical results: the existing test suite passes, and a byte-for-byte or value-for-value comparison of the benchmark workload output before and after is clean. Report any pre-existing test failures separately.
- `git diff` or the file list confirms no dependency manifest or lockfile changes. If the directory isn't a git repo, use another way to show this.
- A short summary of what dominated the time and what you changed.

If p95 < 300 ms can't be reached without breaking exact results, adding a dependency, or changing the protocol, stop. Report the best result you reached under the constraints, where the remaining time goes, and what would be needed. Don't relax any constraint on your own.
```

Notes:
- The prompt doesn't name the repo, benchmark, or commands, because I don't know them. It tells the executor to discover them and not to invent them.
- The prompt states the constraints as fixed, so the executor can't weaken any of them. These are exact results, the same runner and protocol, no new dependencies, and no deployment or merge. If the target can't be reached within them, the executor stops and reports.
- I didn't use `guidance.md` for anything beyond its general advice. That advice is to state the behavior, constraints, authority, and observable checks, and to give a fresh executor everything it needs. No live sources were consulted. The Codex notes I used are dated offline notes, not verified current guidance.