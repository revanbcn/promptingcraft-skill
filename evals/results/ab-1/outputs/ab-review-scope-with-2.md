The prompt contains four distinct tasks. Repeated “Be extremely careful” adds little; concrete verification makes it actionable. Dependency version targets and blog-post details remain unspecified.

```text
Complete all four tasks:
1. Reproduce and fix the failing date-parsing test in utils/dates.test.ts.
2. Refactor the whole utils folder.
3. Upgrade all dependencies.
4. Write a blog post about the completed work, grounded in the actual changes and verified results.

Do not change the public API of formatDate.

Work carefully: run the relevant existing tests and checks to verify the fix and check for regressions from the refactor and dependency upgrades.

Unspecified details: dependency target versions and the blog post’s audience, length, and destination.
```

This preserves the scope and replaces vague emphasis with verification, consistent with [Claude Code’s prompting guidance](https://code.claude.com/docs/en/prompt-library), retrieved through Context7 on October 12, 2026.