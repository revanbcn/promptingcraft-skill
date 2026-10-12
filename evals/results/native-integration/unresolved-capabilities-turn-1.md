The prompt leaves the repository choice open and makes it the executor’s first question.

```text
Investigate why the billing CSV export loses comma-containing names. This is a user-reported defect; the cause has not been established.

This is investigation only. Edits and deployment are not authorized.

Repository choice is unresolved:
api-east and api-west are equally plausible service repositories. Neither has been selected. First ask: “Which repository should I investigate: api-east or api-west?” Wait for the answer before repository-specific investigation. Do not choose based on your working directory, repository names, or apparent relevance.

Your capabilities:
You cannot browse the web and have read-only file access. Use available file-reading tools. Do not assume shell execution is available. Do not perform operations that write files or change state, including checks that generate artifacts.

Any supplied guidance must not be described as current for your environment. Preserve known source dates and provenance; label cached guidance accordingly. If freshness is unknown, say so. The prompt author’s access or retrieval date does not establish freshness or availability for you.

After the repository is selected:
Trace the billing export through the available source and inspect relevant existing tests, fixtures, or export samples. Identify where comma-containing names are lost or altered, without assuming the mechanism in advance.

Report the supported cause with file and line references, or explain why the evidence is insufficient. Distinguish observations, hypotheses, and behavior you could not reproduce. If reproduction requires writes or unavailable capabilities, state that limitation and continue with read-only inspection.
```

Authoring reference: [Claude Code best practices](https://code.claude.com/docs/en/best-practices), retrieved October 12, 2026; this does not establish current guidance for the executor.

