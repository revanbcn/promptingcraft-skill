The original prompt is already suitable. No material revision is necessary.

The source-anchored contract from `task.txt` [local link target omitted]:

| Classification | Exact source anchor |
|---|---|
| EXPLICIT_REQUIRED — outcome | “Fix settings.py so save_settings returns 500 without showing success when the API returns status 500.” |
| EXPLICIT_REQUIRED — invariants | “Preserve the request payload and the status-200 success behavior.” |
| FORBIDDEN — dependencies | “No new dependencies.” |
| EXPLICIT_REQUIRED — scoped authorization | “Local edits and tests are authorized” |
| FORBIDDEN — release actions | “do not commit or deploy.” |
| EXPLICIT_REQUIRED — verification | “Verify both 500 and 200 behavior using the existing tests and report actual results.” |

The original clearly states the defect, preserved behavior, permissions and checks. No material contradiction or omission warrants revision. Executor agent/model and test commands are unspecified; those do not block this handoff. The defect remains user-reported, and existing test coverage was not inspected.

Final outcome: retain `task.txt` exactly. A manual, bidirectional contract review found no additions, omissions or authority drift. This was self-review; no development task or tests were executed.

Source freshness: packaged `knowledge.json` records retrieval and curation on **2026-10-12**, within its seven-day refresh window. That is **dated cached guidance**, not live verification or a publication date. Local contract, rubric and freshness notes have no verifiable retrieval dates, so their freshness is unverified. No live documentation was retrieved.