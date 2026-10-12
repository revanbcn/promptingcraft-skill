Your task is an investigation handoff with no edit authority, so I kept it small. The executor's tools and model are unspecified, so I used general guidance only and made no model-specific tuning.

```
Investigate why the nightly import duplicates invoices, using the provided redacted log and repository. This is read-only.

Return:
- likely causes
- evidence for each (log lines, files and code locations)
- unknowns
- a proposed fix

Constraints:
- Do not edit anything.
- Do not rerun the import.
- Do not access production.
- Do not send messages or publish.
- You may suggest tests for a later authorized fix, but do not run them now.

Context: the log and repository locations are not given here. Find them in your working environment. If you can't find either, say so and list what you couldn't check. Don't guess at their contents.
```

**What I changed and why**
- I kept your wording for the task, the four return items and every prohibition. I added nothing to the constraints.
- I added the context paragraph because a fresh executor can't see your chat or know where "the provided" files are. It only covers discovery and reporting gaps. It adds no new outcome or permission.
- I didn't add edge-case checklists, a required hypothesis format, or a fix-confidence rating. Those would be new requirements you didn't ask for.
- I left the test suggestions as you wrote them (permitted, not required, and not run).

**Source freshness**
- Network retrieval was unavailable. The only guidance I used was your dated `guidance.md` fixture (snapshot 2026-10-10). It is test context, not live-verified official guidance.
- The fixture's advice is to state the desired behavior, context, constraints, authority and observable checks, and not to assume a fresh executor shares your chat history. The prompt follows that.
- That review was a same-model self-check. It doesn't show the prompt will work well on the executor.