The request is blocked on one decision. "Remove all stored customer records" and "retain all customer records for audit" can't both apply to the same records, and no retention policy says which one wins. I haven't picked one. I also haven't added an inventory step, a deletion plan, or any destructive command.

**Deciding question:** Which governs here? Possible answers are:
- (a) Retention wins: nothing is deleted.
- (b) Deletion wins: the audit copy goes too.
- (c) Both apply to different things, for example deletion from live systems with an audit copy kept elsewhere. If so, which records and which systems?

**Blocked handoff (copy as is):**

```
Task (blocked pending a decision): remove all stored customer records, but retain all customer records for audit.

Context:
- These two requirements conflict as written, and no retention policy or decision has been provided. Treat the conflict as unresolved. Do not resolve it yourself by choosing deletion or retention.
- Nothing is known about what customer records exist, where they are stored, or the audit requirements.
- The target agent and model are unspecified. Do not assume a particular one.

Until the user states which requirement governs (or how they apply to different records or systems), do not delete, move, anonymize or alter any customer records. Reply with the deciding question below and wait for the answer.

Deciding question for the user: Should customer records be removed, retained for audit, or both, with each applying to different records or systems? If both, which records and systems does each apply to?

After the user answers, proceed with the resolved task.
```

**Notes**
- **Source of the guidance:** `guidance.md` is a synthetic fixture dated 2026-10-10. No network retrieval was available, so nothing here is live-verified or official. The fixture file is not part of the handoff.
- **What the hold covers:** "Do not delete, move, anonymize or alter" applies only until the user answers. It follows from the unresolved conflict. It isn't a permanent ban and doesn't limit later authorization.
- **Contract check:** Both original statements are preserved. The final prompt adds no new behavior, mechanism or completion gate.