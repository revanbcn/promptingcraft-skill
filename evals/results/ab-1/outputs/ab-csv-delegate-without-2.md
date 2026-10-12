Fix the CSV export with this scope:

- Follow RFC 4180: enclose fields containing commas, double quotes, or line breaks in double quotes; escape embedded double quotes by doubling them; use CRLF record separators.
- Preserve the header and column order exactly: `id,name,status`.
- Add a regression test covering commas, embedded quotes, and multiline values. Assert the exact output and column order.
- Run the relevant tests and report the changes and results.
- Keep the fix focused. Do not deploy.