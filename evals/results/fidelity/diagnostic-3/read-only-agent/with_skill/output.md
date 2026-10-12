The original task is already clear and scoped. I kept its words, added only a short context line and a light output structure, and added no new permissions or completion gates. Nothing here ran. The notes were not live-verified: they are a synthetic fixture dated 2026-10-10, and network retrieval was unavailable. The target agent, its tools and its model are unspecified, so I used no agent- or model-specific tuning.

```
Investigate why the nightly import duplicates invoices, using the provided redacted log and repository.

This is read-only. Do not edit, rerun the import, access production, send messages or publish. You may suggest tests for a later authorized fix, but do not run them now.

Context: the duplication is user-reported. The log is redacted, so some details may be missing. Locate the log and repository yourself; if more than one plausible candidate exists, say which you used. Your available tools are unknown, so work with what you have and say so if something you need isn't available.

Return:
- Likely causes
- Evidence for each (cite log lines and file/line references)
- Unknowns
- A proposed fix

Optional suggestion: where useful, mark which claims are directly evidenced and which are inferred.
```

**Checks against the original request**
- **Preserved:** the investigation goal, the read-only mode, and the four requested outputs. The exclusions on editing, rerunning the import, production, messages and publishing are also kept. The test suggestions stay allowed, and running them stays forbidden.
- **Added, all optional or context:**
  - The redaction and user-reported notes are context.
  - The "which candidate you used" note and the tool-availability note are discovery guidance.
  - The evidenced/inferred marking is labeled as an optional suggestion.
- **Not added:** no mandated root cause, no fix mechanism, no test requirement, and no completion gates beyond the four outputs you listed. I also didn't invent bans on things like commits, since "read-only" already covers them.