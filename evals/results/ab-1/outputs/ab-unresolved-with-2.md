The prompt leaves repository selection open and asks Claude Code to resolve it before investigating.

```text
Investigate why the billing export drops rows. This is investigation only; no edits.

Two equally plausible repositories exist: api-east and api-west. Neither has been selected. First ask me: “Which repository should I investigate: api-east or api-west?” Wait for my answer before repository-specific investigation. Do not choose one yourself or assume both are in scope.

Once I select the repository, use read-only inspection to trace rows from the source through the export and identify where and why they disappear. Examine relevant code and available examples, tests, or logs without changing files or implementing a fix.

Report the findings with file-and-line references and supporting evidence. Distinguish confirmed causes from hypotheses. If the available evidence cannot establish the cause, explain what remains unknown and what specific information would resolve it. Do not claim reproduction or verification that you have not performed.
```

Guidance checked October 12, 2026: [Claude Code best practices](https://code.claude.com/docs/en/best-practices).

