The two requirements conflict, and nothing says which one wins. I haven't drafted a full executor prompt. Below is the deciding question and a short blocked handoff that keeps both statements.

**Deciding question:** Which policy applies to the stored customer records?
1. Delete them from the live stores, but keep an audit copy. If so, where is the copy kept, for how long, and which fields stay?
2. Keep all records, and delete nothing.
3. Something else, such as anonymizing or redacting them.

The handoff below doesn't pick one, because choosing would invent a retention policy.

```
Task (BLOCKED – do not delete or modify any data yet):

The requested work is stated as: "remove all stored customer records, but retain all customer records for audit."

These two requirements conflict as written, and no retention policy or decision has been provided. Deleting the records and keeping them cannot both be done to the same records. Do not resolve the conflict by choosing one yourself.

Until the owner supplies a decision, perform no deletion, overwrite, anonymization, or other data change. Ask the user this one question and wait for the answer:
"Which policy applies: (1) delete from live stores and keep an audit copy (where, how long, which fields), (2) keep everything and delete nothing, or (3) another approach such as anonymization?"

Once the policy is given, carry out that policy, and check that the result matches it.
```

**Notes**
- **Preserved:** Both original statements appear verbatim and with the same strength. The handoff adds no mandatory inventory and no destructive-command plan.
- **Additions:** The no-data-changes-until-decided clause is a safety consequence of the conflict, not a new requirement. The final line is neutral: it applies whatever policy the user gives.
- **Reference context:** `guidance.md` is a synthetic fixture dated 2026-10-10. It is not live-verified official guidance, and I haven't passed it to the executor. The target agent and model are unspecified, so the handoff is agent-neutral.