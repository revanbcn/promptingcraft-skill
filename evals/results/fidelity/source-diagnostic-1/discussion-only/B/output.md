Here is the handoff. I didn't read `validator.py` or `guidance.md`, because this task is compose-only. The prompt tells the executor to read them.

```
Discussion/proposal task, not implementation. Please do not edit any files and do not run tests.

Context: Someone asked, "Could we make validation stricter?" for validator.py. Two alternatives are under discussion:
- A: reject unknown fields.
- B: preserve unknown fields for compatibility.
No implementation decision has been made.

What I need from you:
1. Read validator.py (and any code it directly depends on, if needed) to establish its existing behavior, especially how it currently treats unknown fields. Base the comparison on that observed behavior, and say where you are inferring rather than reading it.
2. Compare A and B: their risks and ideas for verifying each. Verification ideas are proposals only; do not run them.
3. Return a proposal and a list of unresolved decisions. Leave the choice between A and B open unless the code clearly settles it. If you recommend one, label it as a recommendation, not a decision.

Format: a compact table is preferred for the comparison, but it is not required. Use prose where a table fits poorly.

About guidance.md: it is synthetic dated context. Treat it as background only. No usable fresh official retrieval was available when this handoff was written, so do not describe anything in it as current guidance.
```

**Notes**
- **Mode:** I kept this as discussion and proposal. Your "do not edit or run tests" is carried over as written. I did not add any other ban, such as on running commands.
- **Open choice:** A versus B stays unresolved, and any recommendation is labeled as one.
- **Freshness:** No live retrieval was available. The Claude Code notes are cached, dated 2026-10-12, and not live-verified. I made no claim of current guidance.
- **Drift check:** Every instruction in the prompt traces to your wording. The only addition is that the executor should say where it is inferring. That is a clarification of "using the existing behavior", not a new requirement. The table is kept as a preference, and nothing in the prompt makes it a completion gate.