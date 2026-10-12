Here is the handoff. Nothing was executed.

```
In our existing settings UI, Save shows success after a 500 API response. Fix this so Save no longer shows success when the API responds with a 500.

Constraints:
- Preserve the API shape.
- No new dependencies.

Authority:
- Edits and tests are authorized.
- Deployment is not authorized. Do not deploy.

Context:
- The repository paths are not known to me. Find the settings UI's Save flow and the code that handles its API response yourself.
- The 500 behavior is user-reported. Reproduce it first, for example with an existing test or a mocked 500 response, and then fix it.
- What the UI should show after a failed Save is not specified. Follow the UI's existing conventions for showing errors. If there is no clear convention, say so in your report instead of inventing a large new pattern.

Verification:
- Show evidence, such as a test or reproduction, that a 500 response no longer produces the success state, and that a successful response still does.
- Run the project's existing relevant tests and report the actual results, including any failures or tests you could not run.

Optional suggestion: if it is cheap, add a regression test for the 500 case using the project's existing test tooling.
```

- **Mode and scope:** The prompt keeps your four settled points close to your wording: the bug, the API-shape constraint, no new dependencies, and the edit/test/deploy authority. I added no other bans, such as on commits or lockfiles.
- **Unresolved choices:** I left the error UX and the repository paths open, since you didn't specify them. The prompt tells the executor to discover the paths and follow existing UI conventions rather than choose a design.
- **Verification:** The checks only test the requested behavior, that a 500 doesn't show success. The "still works on success" check is there to catch regressions in the same Save flow. The regression test is marked as an optional suggestion, not a requirement.
- **Executor and guidance:** The prompt is written for Codex with an unknown model, so it carries no model-specific tuning. It follows general guidance from the dated, offline fixture (`guidance.md`, 2026-10-10) and the cached Codex notes. Nothing was live-verified, because network retrieval was unavailable.