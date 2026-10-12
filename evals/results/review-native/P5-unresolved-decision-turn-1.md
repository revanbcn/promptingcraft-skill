```text
Investigate why the billing export drops rows. This is investigation only; no edits.

Two equally plausible repositories exist: api-east and api-west. Neither has been selected. First ask: “Which repository should I investigate: api-east or api-west?” Wait for the answer before investigating either repository; do not choose based on the current working directory.

After the repository is selected, use read-only inspection to trace the billing export and determine where the missing rows are excluded or lost. Ground the diagnosis in available code and evidence.

Report the supported cause with file and line references. Distinguish verified findings from hypotheses. If the cause remains unconfirmed, state what evidence is missing and the next read-only check needed. Do not implement a fix.
```

[Claude Code guidance](https://code.claude.com/docs/en/best-practices) checked live on 12 October 2026.

