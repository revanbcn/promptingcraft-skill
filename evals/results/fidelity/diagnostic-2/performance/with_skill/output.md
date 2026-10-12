The prompt is below. I wrote it for Codex and kept your wording where I could.

```
Make the existing 10,000-row benchmark's p95 drop from 900 ms to below 300 ms, measured on the same runner and protocol.

Constraints:
- Exact results must be preserved.
- No new dependencies.
- No deployment.

Context: the benchmark, its runner and its protocol already exist in the repository. Find them yourself. Don't change how the benchmark measures, so that before and after numbers stay comparable.

Verification: report the p95 from the same runner and protocol, before and after your change. Also show evidence that results are exactly unchanged, such as the existing tests or a direct before/after output comparison. Report plainly if the p95 target isn't reached.
```

Notes:
- **Left open:** you didn't name the benchmark, runner or code path, so the prompt tells the executor to discover them. I didn't pick a target or a mechanism such as caching or an algorithm change.
- **Verification:** the checks only restate your two criteria: p95 below 300 ms, and exact results preserved. I added no coverage or process gates.
- **Deployment:** "No deployment" is the only action ban. I didn't add bans on commits or on touching dependency manifests, since you didn't ask for them.
- **Freshness:** the only guidance available was the dated synthetic fixture `guidance.md` (2026-10-10), and I couldn't reach any live sources. I used it as context only, and the prompt doesn't reference it. The executor's model is unestablished, so I applied only general Codex-level guidance.