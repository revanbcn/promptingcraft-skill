Your request didn't say which validation is broken, so the handoff leaves that as a placeholder for you to fill in.

```text
Make a small validation fix in this repository.

Defect to fix: [PASTE THE VALIDATION BUG HERE: what input or case is handled wrongly, what happens now, and what should happen instead. This was not specified when the handoff was written. If it is still missing and the target is unclear or ambiguous, ask which validation is meant instead of guessing.]

Constraints:
- Preserve API shape.
- Do not deploy.

Context:
- You don't have the author's chat history. Find the relevant code yourself.
- Reproduce the reported failure before changing anything, then confirm it is fixed afterward. Use whatever test or check the repo already provides, or a direct call to the validation.
- Show the evidence of the before and after behavior in your final report.

Optional suggestion: if the repo has an existing test suite, run it once at the end to check that nothing else regressed.
```

Notes on what I did and didn't do:
- **Contract kept:** "small validation fix", "Preserve API shape" and "do not deploy" are carried over without exceptions. I added no bans on commits or other stages, and no instruction to skip planning.
- **Unresolved:** the actual bug and its location. I left a placeholder because I don't know which validation is meant, and guessing one would change the scope.
- **Guidance freshness:** you said the only guidance is a cached summary checked in 2024, with no network access. I treat that as stale, offline guidance, not live-verified or current. It only supports the general approach of stating the outcome, giving context and constraints, and including a check the executor can run. The executor's model is unknown, so I applied no model-specific tuning.
- **Reference file:** I didn't put `guidance.md` into the handoff, because the executor isn't known to have it.
- **Drift check:** every directive in the prompt traces to your request or to the context needed to verify the fix. The test-suite line is marked as an optional suggestion and isn't a completion requirement.