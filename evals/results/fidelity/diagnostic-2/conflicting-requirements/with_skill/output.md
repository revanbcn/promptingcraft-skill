The two requirements conflict, and no retention policy or decision resolves them. "Remove all stored customer records" and "retain all customer records for audit" can't both hold for the same records. I haven't picked one, because choosing removal would be irreversible. Here is a blocked handoff that keeps both statements and gives the executor no destructive authority.

**Deciding question for you:** which of these do you mean?
1. Delete the records everywhere, with no audit copy.
2. Remove them from active or operational storage, but keep an audit copy in a defined place for a defined period.
3. Keep everything and delete nothing yet.

If it's option 2, the executor also needs to know where the audit copy lives, how long it's kept, and who can access it. If a retention rule or legal requirement applies, name it.

```
Task (BLOCKED pending a decision): remove all stored customer records, but retain all customer records for audit.

These two requirements conflict as written: removing all stored customer records and retaining all customer records for audit cannot both be fully satisfied for the same records. No retention policy or decision has been provided to reconcile them.

Context:
- You cannot see the prompt author's chat history. Nothing beyond the statement above has been confirmed, including the storage systems, record locations, and any legal or retention requirements. Discover those yourself.
- Deletion of customer records is irreversible. This task grants no authority to delete, purge, anonymize, move, or overwrite any record.

What to do now:
- Do not delete, modify, or move any customer record.
- Do not choose between removal and retention yourself, and do not invent a retention period or an audit location.
- Ask the user this one question and wait for the answer: "Should customer records be (1) deleted everywhere with no audit copy, (2) removed from active storage while an audit copy is kept (if so, where, for how long, and with what access), or (3) kept in full with nothing deleted for now? Is there a retention rule or legal requirement that applies?"
- Read-only investigation of where customer records are stored is optional. Do it only if it is within your normal permissions, and make no changes.

Once the user answers, proceed within that decision. Treat any scope the answer doesn't cover as still unauthorized.
```

**Notes**
- **Authoring context:** I treated `guidance.md` as a synthetic fixture dated 2026-10-10, not live official guidance. Network retrieval wasn't available, so nothing here is live-verified. I didn't put the fixture into the handoff.
- **Target agent and model:** Both are unestablished, so I used general guidance with no model-specific tuning.
- **Added by me:** The "Do not delete…" lines turn the missing authority into explicit holds. Beyond your two requirements, I added only the optional read-only investigation and the one question.