Fix the CSV export with these requirements:

- Follow RFC 4180 quoting: enclose fields containing commas, double quotes, CR, or LF in double quotes. Escape embedded double quotes by doubling them.
- Keep the column order exactly `id,name,status`.
- Add a regression test covering commas, embedded quotes, and line breaks, and assert the column order.
- Keep the change focused, run the relevant tests, and report the changes and results.
- Do not deploy.