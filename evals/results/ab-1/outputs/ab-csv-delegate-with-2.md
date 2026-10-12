```text
Fix the CSV export with these requirements:

- Apply RFC 4180 quoting: enclose fields containing commas, double quotes, or line breaks in double quotes. Escape embedded double quotes by doubling them.
- Keep the column order exactly id,name,status.
- Add a regression test covering commas, embedded double quotes, and multiline values. Assert correct quoting and the exact column order. Confirm it fails before the fix and passes afterward, then run the relevant existing tests.
- No deployment. Do not take actions that trigger an automatic deployment.
```

Quoting rules verified against [RFC 4180, Section 2](https://www.rfc-editor.org/rfc/rfc4180#section-2).