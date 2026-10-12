Here is the handoff. I only composed it and did not run the task. The guidance came from the supplied `guidance.md`, which says it was verified externally on 2026-10-12. I had no live retrieval and did not fetch the page myself. The Claude Code notes are dated cached guidance. I didn't establish which model the executor runs.

```
Prepare a proposal comparing queue designs. This is a proposal task only: implementation is not authorized, so do not make code changes or implement any of the designs. Reading the codebase and planning are allowed.

Immutable manifest. Preserve it exactly, including order and punctuation. Do not alter, reformat, reorder or summarize it, and quote it verbatim wherever the proposal refers to it:
{"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}

Constraints:
- No new dependencies.

Context and open items:
- The task doesn't say which queue or system the designs apply to, or which designs to compare. If the codebase makes this clear, use what you find. If several equally plausible targets exist, say so in the proposal and ask which one is meant. Don't choose one silently.
- No output location or format for the proposal is specified. Deliver it in your reply unless the user says otherwise.

Optional suggestion: discuss monitoring separately from the main design comparison.
```

**Notes on the handoff**
- **Mode:** I kept it as a proposal. "Implementation is not authorized" is stated as a prohibition, and planning is explicitly allowed.
- **Manifest:** I copied it character for character and marked it immutable.
- **Dependencies:** "No new dependencies" is kept as written. I did not add a freeze on manifest or lockfile files.
- **Monitoring:** It stays an optional suggestion and is not an acceptance gate.
- **Unresolved scope:** I left open which queue or system is meant and which designs to compare. I added no output file, no criteria for choosing between designs, and no checks beyond what you asked for.