Here is the handoff. I wrote it without opening `validator.py`, so nothing in it describes the file's actual behavior.

```
Task: analysis only. Read validator.py and report back. Do not edit any files and do not run tests.

Context
- We're considering making validation stricter in validator.py. No implementation decision has been made.
- Two alternatives are on the table:
  A. Reject unknown fields.
  B. Preserve unknown fields for compatibility.
- I haven't seen the code in this handoff, so any claim about current behavior must come from what you read in validator.py (and any callers or tests you read to understand it). Don't assume it from this prompt.

What I want
1. Use the existing behavior of validator.py as the baseline. Describe how it currently treats unknown fields, citing file and line references.
2. Compare A and B. Cover the risks of each, and ideas for verifying each one, grounded in that existing behavior. A compact table is preferred, but not required.
3. Return a proposal and a list of unresolved decisions. The proposal should not claim that a choice has already been made.

Constraints
- Do not edit files.
- Do not run tests. Reading code and existing tests is fine.
- Do not implement either alternative.
- Mark clearly anything you are inferring rather than seeing in the code.
- If validator.py can't be found or read, say so and stop. Don't guess at its contents.
```

**Notes**
- **Executor and model:** The target is Claude Code. The model is unknown, so I used agent-level guidance only.
- **Guidance used:** `guidance.md` is a synthetic fixture dated 2026-10-10. The Claude Code notes are cached offline, last checked 2026-10-12. Neither is live-verified, and I did no retrieval.
- **Left out on purpose:** I added no code facts, commands, test names, thresholds or recommendations. Which option to choose stays open. The "stop if unreadable" line only stops the executor from fabricating, and I don't count it as a new requirement.
- **Drift check:** I compared the final text against your request in both directions. Every operative clause traces to your wording or is a direct breakdown of it. The only judgment calls are allowing reads of callers and tests, which I read as part of "using the existing behavior", and the instruction to mark inferences.