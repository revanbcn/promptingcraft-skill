Here is the handoff. I used the Codex notes dated 2026-10-12 and the `guidance.md` fixture dated 2026-10-10. Neither is live-verified, because network retrieval was unavailable. The executor model is unknown, so I added no model-specific tuning.

```text
In our existing settings UI, Save shows success after a 500 API response. Fix this.

Context:
- Exact repository paths are unknown. Find the settings UI and its Save handler, and the code that calls the API, by searching the repository.
- If several places could equally be "the settings UI" Save, don't guess. Report the candidates and ask which one I mean.

Constraints:
- Preserve the API shape.
- No new dependencies.

Authority:
- You may edit files and run tests.
- Do not deploy.

Verification:
- Show observable evidence that Save no longer shows success after a 500 response. A test that simulates a 500 is a good way to do this, using the repository's existing test setup.
- Run the relevant existing tests and report the results, including any failures or tests you could not run.
```

Notes on what I did:
- **Kept from your request:** the bug, "preserve the API shape" (unconditional, with no exceptions), "no new dependencies", edits and tests authorized, and deployment not authorized.
- **Not added:** how the failure should be displayed, whether to keep the user's edits, and handling for other network errors. You didn't specify these, so the executor decides them. Say so if you want them pinned down.
- **Unknown paths:** I treated them as normal discovery. I added one narrow stop: if there are several equally plausible Save targets, the executor asks instead of picking one.
- **No other bans:** I didn't add restrictions on commits or on dependency manifests, since you didn't ask for them.