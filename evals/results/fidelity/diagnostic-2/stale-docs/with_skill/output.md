Here's the handoff.

```
Make a small validation fix. Preserve API shape. Do not deploy.

Context:
- This prompt doesn't say which validation is wrong or what the expected behavior is. Find that in the repository, issue or task notes you have. If you can't identify a single target or the intended behavior, ask me before changing anything.
- You can't see the chat this prompt came from, so check anything you rely on against the repository.

Verify directly:
- Show that the specific validation behavior you fixed now works. Use a test, build or other check you can actually run here.
- Show that the API shape is unchanged, and report the evidence you obtained.
- If a check couldn't be run, say so.
```

- **Unresolved:** you didn't say which validation is broken or what correct behavior is. I left that open with a "ask if it can't be identified" step. I didn't invent a target.
- **Kept as written:** "Preserve API shape" has no exceptions. "Do not deploy" bans only deployment. I didn't add bans on commits or other stages, and I didn't add a "skip planning" instruction.
- **Source freshness:** the only guidance was your cached summary, which you said was checked in 2024. That makes it stale as of 2026-10-12, and I had no network access to refresh it. The `guidance.md` in the working directory is a synthetic fixture (snapshot 2026-10-10) and doesn't update that 2024 date. I used it only as general context about specifying outcome, constraints, authority and checks. Nothing in the prompt claims live or official sources.
- **Executor model:** the model is unestablished, so I applied only general Claude Code guidance, with no model-specific tuning. I didn't pass `guidance.md` to the executor.
- **Review:** this was a self-review only. Every clause traces to your three constraints, or to a plain restatement of them as checks. I added no optional suggestions.