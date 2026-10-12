```text
Fix the dashboard CSV export bug: users report that rows appear in the UI, but the export loses names containing commas.

Preserve these agreed constraints:
- Use the existing export action.
- Preserve the existing columns and order exactly: id,name,status.
- Add no new dependencies.
- Leave auth unchanged.

Implementation and relevant regression verification are authorized. Deployment is not authorized; do not deploy or trigger deployment.

Locate the export implementation, reproduce the reported issue, and fix its cause. Add and run relevant regression verification covering a comma-containing name such as "Doe, Jane" and a name without commas. Verify that each name survives intact as one CSV field, with the corresponding id and status preserved and columns ordered id,name,status.

Report the change, verification performed and results, and any remaining limitations.
```

Prepared using [official Codex prompting guidance](https://learn.chatgpt.com/docs/prompting#use-editor-context), retrieved 2026-10-12.

