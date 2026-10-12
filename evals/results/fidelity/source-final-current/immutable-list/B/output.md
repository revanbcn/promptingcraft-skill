The original task already holds up, so I made only light edits: I put it in handoff form and kept the manifest verbatim. I added no requirements.

```
Prepare a proposal comparing queue designs.

Implementation is not authorized. Planning is allowed. Do not edit project files to implement any design.

Preserve this immutable manifest exactly, including order and punctuation:
{"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}

No new dependencies.

Optional suggestion: discuss monitoring separately.
```

**Review notes**
- **Mode:** I kept this as a proposal. Comparing designs gives no edit authority, and the prompt says so. It also says planning is allowed, as you did.
- **Manifest:** It is copied character for character. I added no interpretation of how it relates to the queue designs.
- **No new dependencies:** It forbids adding dependencies. It does not freeze manifest or lockfile files.
- **Monitoring:** It stays marked "Optional suggestion" and is not an acceptance check.
- **Left open:** You didn't name which queue designs to compare or what to base the comparison on. The executor can discover that from the project, and I did not invent candidates or criteria. If several scopes seem equally plausible, you may want to name the designs yourself.
- **Not included:** Nothing about the deliverable's format or location, and no `guidance.md` content.
- **Source freshness:** `guidance.md` is a synthetic fixture dated 2026-10-10, and no live retrieval was available. The Claude Code notes are dated cached guidance, so I make no claim that they are current. The target model is not established, so I used no model-specific tuning.
- **Drift check:** I compared the original against the final in both directions. Every original item appears in the handoff with the same strength, and every clause in the handoff traces to your words.