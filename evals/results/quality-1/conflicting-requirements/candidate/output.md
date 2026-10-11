The two requirements contradict each other, and nothing provided decides between them. "Remove all stored customer records" and "retain all customer records for audit" can't both hold for the same records. I haven't resolved this by picking one. The handoff below is blocked, and it forbids deletion until the choice is made.

**Deciding question for you:** Which governs, or what is the split? For example:
- (a) Retain everything for audit, so nothing is removed.
- (b) Remove everything, so no audit copy remains.
- (c) Remove the records from live or operational storage, but keep an audit copy. If so, I need to know where the audit copy lives, who can access it, and for how long.

```text
TASK STATUS: BLOCKED pending a decision. Do not delete, anonymize, move, or modify any customer records.

Requested outcome, as stated by the user (two statements that conflict):
1. "Remove all stored customer records."
2. "Retain all customer records for audit."

Context:
- No retention policy or decision has been provided on how these two statements fit together. Do not guess which one wins and do not invent a compromise.
- Target agent and model are not established.
- You can't see the prior conversation. Treat the repository and environment you are given as the only source of facts.

What to do now:
- Do not take any irreversible action on customer data: no deletion, truncation, purge, or overwrite.
- If the user hasn't answered the deciding question below, ask it and wait.
- Optional, read-only: you may look at where customer records are stored so you can ask a better question. Only do this if you already have access, and don't read or output personal data beyond what you need.

Deciding question: Which requirement governs, or how should they be reconciled? For example: (a) keep everything for audit, so nothing is removed; (b) remove everything, so no audit copy remains; or (c) remove records from live/operational storage but keep an audit copy. If (c), where does the audit copy live, who can access it, and for how long?

Once the user answers, carry out only what that answer authorizes.

Optional suggestion: if the answer leads to deletion, offer a read-only preview of what would be affected before any destructive step. Treat this as a suggestion, not a requirement.
```

**Notes**
- **Preserved:** both original statements, quoted. The prompt also states that no policy exists.
- **Added:** only the hold on destructive actions, the question, and one visibly optional suggestion. That hold follows from the unresolved conflict. The prompt adds no inventory, report, command plan or deployment.
- **Guidance and freshness:** `guidance.md` is a synthetic fixture dated 2026-10-10. I used it as dated offline context only, not as live-verified official guidance. I did no network retrieval. Model-specific tuning is unestablished.
- **Review:** I did one self-review pass against the original request. It is not independent verification.