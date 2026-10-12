Here is the Codex task. I didn't implement or run anything.

```text
Task: Make the existing 10,000-row benchmark's p95 latency drop from 900 ms to below 300 ms. Measure it on the same runner and with the same protocol as the current 900 ms figure.

Requirements
- The benchmark's p95 must be below 300 ms. The current p95 is 900 ms. Use the same runner and the same protocol for both numbers. Don't change the benchmark's runner, protocol or row count to get a better number.
- Exact results must be preserved. The optimized code must return exactly the same results as before.
- Add no new dependencies.
- Do not deploy.

Context
- You have no access to my chat history. Find the benchmark and the code it exercises in the repository. I haven't named any paths.
- If the repository contains more than one plausible 10,000-row benchmark, or the runner or protocol behind the 900 ms figure can't be identified, stop and ask which one I mean. Don't pick one yourself.

Verification
- Before changing anything, record the benchmark's p95 and its exact outputs as a baseline. Use the existing runner and protocol.
- After the change, rerun the same benchmark the same way. Report the before and after p95 values, and show that the results match the baseline exactly.
- If you can't reach p95 below 300 ms, report the best p95 you reached and what limits it. Don't say the target was met when it wasn't.
```

**Notes**
- **Guidance used:** I used the dated Codex routing notes and the `guidance.md` fixture (snapshot 2026-10-10). Neither is live or official, because network retrieval was unavailable. The model that will run the task is unknown, so I added no model-specific tuning.
- **Open choice:** You gave no benchmark path, runner or protocol. The prompt leaves that to discovery and asks the executor to stop if several benchmarks fit. I didn't invent a path, a profiler or an optimization method.
- **Authority:** The prompt grants no authority beyond your words. "No deployment" is the only action ban, and I didn't add bans on commits or manifest changes.
- **Checks:** The verification steps only check the stated outcome: p95 below 300 ms, and results identical to the baseline.