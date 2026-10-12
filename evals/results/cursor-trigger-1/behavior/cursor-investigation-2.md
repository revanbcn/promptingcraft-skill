```text
You are Cursor Agent running in Auto model selection mode.

Task: Investigate why the search page sometimes shows stale results after a product is edited.

Known context:
- This is intermittent (“sometimes”).
- We do not yet know whether the issue is caused by:
  1) caching,
  2) the indexing pipeline/indexer,
  3) client-side behavior.
- Product has NOT decided whether stale results for up to 1 minute are acceptable.

Scope and constraints:
- Investigation only.
- Do NOT modify code, configs, or infrastructure.
- Do NOT create commits, branches, PRs, migrations, or deploy actions.
- Read-only exploration is allowed (code reading, logs/telemetry inspection if available, local reproduction attempts, running non-mutating commands/tests).

What to do:
1) Map the end-to-end flow from “product edit” to “search result visible”:
   - write path (edit API/service),
   - persistence layer,
   - indexing trigger + indexing completion,
   - cache layers (server/CDN/app/query/client),
   - search read path + client rendering/state updates.
2) Produce a hypothesis matrix for cache vs indexer vs client:
   - expected symptom pattern for each,
   - evidence that supports/weakens each,
   - what to check next to disambiguate.
3) Try to reproduce locally or from available logs/observability traces:
   - capture timing of edit event vs search freshness,
   - identify whether stale response is already stale at API boundary or becomes stale in client state.
4) Identify current freshness behavior and implicit SLA:
   - what freshness window is currently observed in practice,
   - whether behavior appears eventual-consistency-by-design or a bug/regression.
5) Keep the unresolved product decision explicit:
   - do not assume that “<= 1 minute stale” is acceptable or unacceptable.

Output format (single investigation report):
- **Executive summary**: most likely fault domain (cache/indexer/client) with confidence level.
- **Evidence**: concrete findings (files, logs, traces, timestamps, request/response behavior).
- **Flow map**: concise step-by-step system path from edit to search.
- **Hypothesis matrix**: cache vs indexer vs client, with supporting/contradicting evidence.
- **What is unknown**: blocking gaps in telemetry, reproducibility, or environment.
- **Decision support for Product**:
  - If stale <= 1 minute is accepted, what system behavior would be considered OK.
  - If not accepted, what gap likely needs fixing first.
- **Next steps (no code changes)**: highest-value validation steps and instrumentation checks.

Important:
- If evidence is insufficient to isolate one domain, say so explicitly and rank likely causes.
- Prefer precise, testable statements over speculation.
- Keep everything investigation-only and read-only.
```
