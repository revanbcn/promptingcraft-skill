The handoff is below. I didn't run the task or touch any files.

```
Prepare a proposal comparing queue designs. Implementation is not authorized.

Mode: this is a proposal and planning task. Planning is allowed. Do not implement any of the designs.

Preserve this immutable manifest exactly, including order and punctuation. If your proposal quotes or refers to it, copy it verbatim:
{"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}

Constraint: no new dependencies.

Context you should know:
- You don't have this conversation. The working directory is [AUTHOR_WORKSPACE_PATH_REDACTED]. Look through it for any existing code or notes on queues.
- Which queue designs to compare has not been specified. Pick candidates from what you find, or from well-known designs. Say which you chose and why. If the candidates are unclear and the choice matters, ask one focused question.

Optional suggestion: discuss monitoring separately.
```

**Contract check against your original request**
- **Kept as written:** the manifest is verbatim, "Implementation is not authorized", "No new dependencies" and "Planning is allowed". I left out any ban on editing manifest or lockfile bytes, since you didn't ask for one.
- **Kept optional:** monitoring stays under "Optional suggestion:" and is not a completion gate.
- **Left open:** you didn't name the queue designs to compare, so the handoff doesn't pick them. I added no acceptance gates, tests or thresholds.
- **My additions:** the working-directory line and the "say which you chose and why" instruction are context and clarification, not requirements. You didn't say how to deliver the proposal, so I left that open.

**Freshness:** I found no usable retrieval of official guidance. I relied on the dated offline Claude Code notes (summary checked 2026-10-12) and the synthetic `guidance.md` (snapshot 2026-10-10). Neither is current or live-verified guidance. The target model is unestablished, so I applied no model-specific tuning.

**Review:** I did one self-review pass, which is not independent verification. It found no omissions, strengthened options or new authority.