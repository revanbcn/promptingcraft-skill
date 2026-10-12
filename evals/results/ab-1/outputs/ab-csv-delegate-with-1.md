```text
Fix the CSV export:

- Quote fields per RFC 4180: wrap fields containing commas, double quotes, or line breaks in double quotes, and escape embedded double quotes by doubling them.
- Keep the column order exactly id,name,status.
- Add a regression test covering quoting, escaping, and column order. Confirm it fails before the fix and passes afterward; run relevant existing tests.
- Do not deploy or trigger deployment through another action.
```

Quoting details follow [RFC 4180, section 2](https://www.rfc-editor.org/info/rfc4180/), checked October 12, 2026.