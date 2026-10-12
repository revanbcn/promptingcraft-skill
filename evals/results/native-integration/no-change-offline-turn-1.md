The original prompt is already suitable. No material revision is necessary.

It clearly defines the outcome, constraints, authority, and verification. Review used dated Codex references checked 2026-10-12; current documentation was unavailable.

```text
Fix the CSV export so names containing commas survive a CSV parse round trip. Preserve the existing columns and their order: id,name,status. Use the existing export action, add no dependencies, and preserve authentication behavior. Implementation and relevant regression tests are authorized. Do not deploy. Verify the round trip with a comma-containing name and an ordinary name, and run the affected existing tests.
```

