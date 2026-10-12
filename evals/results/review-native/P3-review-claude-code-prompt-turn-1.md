The repeated “Be extremely careful” adds no concrete guidance. This version preserves all four tasks and makes verification explicit.

```text
Complete all four tasks:

1. Reproduce the failing date-parsing test in utils/dates.test.ts, identify the cause, and fix it.
2. Refactor the whole utils folder while preserving intended behavior.
3. Upgrade all dependencies and address compatibility issues introduced by the upgrades.
4. Write a blog post about the completed fix, refactor, and dependency upgrades, grounded in the actual changes and verification results.

Do not change the public API of formatDate.

Verify that utils/dates.test.ts passes, run the project's existing checks relevant to the refactor and dependency upgrades, and confirm that formatDate's public API remains unchanged.

Unspecified choices: dependency target versions and the blog post's audience and length.
```

The emphasis on specific constraints follows [Claude Code’s guidance](https://code.claude.com/docs/en/best-practices#provide-specific-context-in-your-prompts), retrieved October 12, 2026.

