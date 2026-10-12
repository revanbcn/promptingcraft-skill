The source is a dated synthetic fixture, with no live retrieval. The handoff doesn't depend on it, and it isn't passed to the executor. I wrote it for Codex but assumed no model. Which benchmark to run is left for the executor to find. I added no commands, file paths, or approaches, and no ban on commits or on touching dependency manifests.

```text
Task: Reduce latency of the existing 10,000-row benchmark.

Goal: The existing 10,000-row benchmark currently has a p95 of 900 ms (user-reported). Bring it below 300 ms on the same runner and protocol.

Constraints:
- Exact results must be preserved.
- No new dependencies.
- No deployment.

Context:
- Locate the existing benchmark and its runner/protocol in the repository. Don't change the benchmark's runner or protocol to obtain the improvement.
- Start by reproducing the reported ~900 ms p95 baseline with that benchmark, and keep a record of the baseline results so you can compare them with the results after your change.

Verify:
- Re-run the same benchmark on the same runner and protocol, and report the before and after p95 values. The after value must be below 300 ms.
- Show that the results are exactly the same as the baseline results.
- Run the project's existing tests, if any, and report the outcome.

Optional suggestion: profile first to find where the time goes before changing code.
```