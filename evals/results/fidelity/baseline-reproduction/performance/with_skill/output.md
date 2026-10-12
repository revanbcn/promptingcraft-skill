The prompt is below. I haven't run or inspected anything.

```
Task: make the existing 10,000-row benchmark faster. Its p95 latency is currently 900 ms. It must come in below 300 ms.

Requirements
- Measure on the same runner and with the same protocol as the existing benchmark. Don't change the benchmark's runner, protocol or dataset to get the number down.
- Results must stay exactly the same. Output for the same inputs must be identical to what the code produces today.
- Add no new dependencies.
- Do not deploy. Don't push, publish or release anything either.

Context you need to find yourself
- I haven't named the benchmark, its command or the code path it exercises. Locate the existing 10,000-row benchmark in the repository first, and work out how it's run and how it reports p95.
- If you can't find it, or its runner or protocol is ambiguous, stop and ask. Don't substitute your own benchmark.

Verification (report evidence, not assertions)
- Record the baseline p95 from the existing benchmark, using its own protocol, before you change anything. Report it next to your numbers. The 900 ms figure above is my own figure, so confirm it.
- Report the final p95 from that same benchmark, and say whether it is below 300 ms.
- Show that results are exactly unchanged. Compare outputs from before and after on the benchmark's inputs, and run the existing tests.

In your final message, summarize what you changed and why it's faster. Also report the before and after p95 figures and the outcome of the exact-results comparison. If you can't reach 300 ms while preserving exact results, say so and report the best result you got. Don't relax any of the constraints above.
```

- **What the prompt keeps from your request:** the 900 ms to under 300 ms target, the same runner and protocol, exact results, no new dependencies and no deployment.
- **What it leaves open:** I didn't name the benchmark, its command or the code path, because I don't know them. The executor has to find the benchmark and ask if it's ambiguous.
- **What the checks cover:** they only test your stated goals. They are a baseline p95 on the existing protocol, a final p95, and an exact-output comparison.
- **What I added:** the "confirm 900 ms" step, the instruction to report the best result if 300 ms can't be reached, and the ban on pushing, publishing or releasing. These are my additions, not yours. Remove any you don't want.
- **Sources:** I used only the dated, offline Codex notes and `guidance.md`, which is a synthetic fixture. Nothing was checked live, and the executor's model is unknown.