```text
Fix the team dashboard CSV export bug: names containing commas currently split across columns.

Implementation is approved. Deployment is not approved; do not deploy or trigger an automatic deployment.

Requirements:
- Keep the columns and order exactly id,name,status.
- Reuse the existing export action.
- No new dependencies.

Locate the existing export code, reproduce the reported failure, and implement the fix so comma-containing names remain intact in the name column.

Verify through the existing export action that:
- A name containing a comma is preserved as one field.
- Each exported row retains exactly three columns in the required order, with id and status correctly aligned.
- Names without commas continue to export correctly.

Run the relevant existing checks and summarize the fix and verification results.
```

Checked against [official Codex prompting guidance](https://learn.chatgpt.com/docs/prompting#cli-workflow-tight-loop-with-reproduction-and-verification) on 2026-10-12.