The scope contains four tasks. Keep them explicit, and replace repeated caution with concrete verification steps.

```text
Complete all four tasks:

1. Diagnose and fix the failing date-parsing test in utils/dates.test.ts. Address the underlying cause; do not skip or weaken the test to make it pass.
2. Refactor the entire utils folder.
3. Upgrade all dependencies and resolve any resulting compatibility issues.
4. Write a blog post explaining the date-parsing fix, the utils refactor, and the dependency upgrades.

Hard constraint: Do not change the public API of formatDate.

Before editing, inspect the relevant code and reproduce the failing test. Make changes in separate, reviewable steps so failures can be traced to their cause.

Verify the date-parsing fix with the focused test, run the utils tests after the refactor, and run the full test suite and available project checks after the dependency upgrades.

Base the blog post on the completed work and actual verification results. Finish with a concise summary of changes, checks performed, any unresolved issues, and the blog post’s location.
```