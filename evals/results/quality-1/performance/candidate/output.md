Here is the Codex handoff. I composed it only and ran nothing.

```text
Goal: Make the existing 10,000-row benchmark's p95 latency drop from the current 900 ms to below 300 ms. Measure it on the same runner and with the same protocol as the current benchmark.

Context:
- You can't see the author's chat history. Find the benchmark and the code it exercises in the repository yourself.
- The 900 ms p95 is the figure the requester reported. The requester gave no benchmark command, file paths or runner details.
- The requester didn't say how "exact results" are defined or checked. Use the repository's existing tests or outputs to establish that.

Constraints:
- Exact results must be preserved. The optimized code must return the same results as before.
- Don't add any new dependencies.
- Don't deploy anything.
- Don't change the benchmark's runner, protocol or 10,000-row workload to get a better number. The comparison has to be like-for-like.

Acceptance (verify these directly and report the evidence):
- Run the existing benchmark unchanged, on the same runner and protocol. Report that p95 is below 300 ms, and include the measured number.
- Show that results are identical to the pre-change results. Use the existing tests or output comparison.
- Confirm that the dependency manifests and lockfiles are unchanged, and that nothing was deployed.

If you can't meet a requirement, say which one and why. Don't claim success without the measurements.

Optional suggestion: Profile the benchmark first to find the dominant cost before changing code.
```

- **Preserved from your request:** the 900 ms to under 300 ms target, the same runner and protocol, exact results, no new dependencies and no deployment.
- **Added:** a ban on altering the benchmark to improve the number. This follows from "same runner and protocol".
- **Acceptance checks:** they only verify what you asked for. I added no coverage targets, repeat-run counts or extra gates. Profiling first is marked optional.
- **Left open:** the benchmark command, the file paths and what counts as "exact" are for the executor to discover. I didn't invent them.
- **Executor and sources:** I treated the executor as Codex with an unknown model. `guidance.md` is a dated synthetic fixture (2026-10-10), and no live retrieval was available, so the Codex guidance is cached and not live-verified.