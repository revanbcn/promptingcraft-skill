Here is the handoff. I didn't execute the task.

```
Prepare a proposal comparing queue designs. Implementation is not authorized.

Preserve this immutable manifest exactly, including order and punctuation:
{"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}

Constraints:
- No new dependencies.
- Planning is allowed.

Context: the task doesn't name the queue designs to compare or the codebase they apply to. Use the working directory for read-only context if it helps. If the candidate designs are unclear, state which ones you chose to compare and why.

Optional suggestion: discuss monitoring separately.
```

**Notes**
- **Mode:** I kept this as a proposal. "Implementation is not authorized" is carried over as written, and I added no edit or commit rules. "Planning is allowed" is preserved as given.
- **Manifest:** I copied it character for character, in the same order and with the same punctuation.
- **Monitoring:** It stays marked as an optional suggestion inside the prompt, and it isn't a completion gate.
- **Open choices:** You didn't say which queue designs to compare or what the target codebase is. I left both open instead of inventing them. The handoff lets the executor read the working directory and state its chosen candidates. If you want specific designs compared, tell me and I'll add them.
- **Guidance and freshness:** I used `guidance.md` only as authoring reference and kept it out of the handoff. It was supplied as externally verified on 2026-10-12. I did no live retrieval and didn't fetch that page myself. The guidance is general Claude Code advice, not tuning for a specific model.
- **Drift check:** I compared the final text against your original in both directions. Nothing was added or dropped, and the one clause beyond your wording is the context paragraph on open choices.