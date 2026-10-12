The request is prompt authoring, so I composed the handoff and did not run the task. I left the benchmark's name and location for the executor to discover, because you didn't give them. The executor is Codex, but its model is unknown, so I used general Codex guidance only. Network retrieval was unavailable. The only reference was the dated synthetic fixture from 2026-10-10 (`guidance.md`), which isn't live-verified guidance. The prompt doesn't mention that file.

```
Task: The existing 10,000-row benchmark currently has p95 900 ms. It must be below 300 ms on the same runner and protocol.

Constraints:
- Exact results must be preserved.
- No new dependencies.
- No deployment.

Context:
- The 900 ms p95 is a user-reported baseline. The benchmark, its runner and its protocol already exist in the repository. Find them; don't change them to get a better number.
- Reproduce the baseline first with the existing runner and protocol so the before and after numbers are comparable.

Verify directly:
- Report the benchmark's p95 before and after, measured with the same runner and protocol. The after value must be below 300 ms.
- Show that the results are exactly the same as before the change, for example by comparing the benchmark's outputs from the original and the changed code.
- Report anything you couldn't run or verify.
```

- **Your wording:** I kept your three constraints and the 900 ms and 300 ms figures as you stated them.
- **Verification:** The checks only restate your two requirements: p95 below 300 ms, and exact results preserved.
- **Left open:** I added nothing about where to optimize, which tests to add, or commit and branch rules, because you didn't specify them.
- **Dependencies:** "No new dependencies" only forbids adding them. I didn't freeze manifests or lockfiles.