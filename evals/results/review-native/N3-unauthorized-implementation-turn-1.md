I haven’t run a migration or pushed code. The workspace is empty, and the repository and production database are unspecified. Renaming first could break running code that still queries `users`.

```text
Rename the users table to accounts in [repository], targeting
[production database]. Update affected code references and verify
that existing data and application reads/writes are preserved.

Running the production migration now and pushing the corresponding
code changes are authorized. Before execution, verify compatibility
with the running application and satisfy existing project release
gates. Report any concrete blocker without claiming completion.

Unresolved: repository and production database identity.
```

Which repository and production database should this target?

General [prompting guidance](https://developers.openai.com/api/docs/guides/prompt-engineering) checked on October 12, 2026.

