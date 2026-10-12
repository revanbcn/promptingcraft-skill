Using `promptcraft` to produce an execution-ready handoff for Cursor Agent (Auto), preserving your exact scope and unresolved product decision.

```text
You are Cursor Agent (Auto). Investigation only.

Context:
- Our search page sometimes shows stale results after a product is edited.
- We do not yet know whether the fault is in cache behavior, indexing latency/failure, or client-side behavior.
- Product has not decided whether stale results for up to 1 minute are acceptable.

Task:
Investigate and determine where staleness is introduced, without making code or config changes.

Hard constraints:
- Do NOT modify code, tests, configs, infrastructure, or data models.
- Do NOT commit, deploy, run migrations, or change cache/index settings.
- Read-only investigation and non-destructive diagnostics only.

What to do:
1) Reproduce the issue
- Identify a reliable repro flow: edit a product, then query/search for it.
- Capture timestamps for: edit write time, index update visibility (if observable), and search UI result update.

2) Trace the pipeline end-to-end
- Product edit path (write path + any events/jobs)
- Indexer path (enqueue, processing, success/failure/latency signals)
- Search serving path (cache keys/TTL/invalidation behavior)
- Client path (request timing, response handling, local cache/state reuse)

3) Isolate first point of staleness
- Determine where fresh data diverges from shown result first:
  - backend cache layer
  - index not updated yet / delayed
  - client showing cached/stale response or state
- Provide evidence for each component ruled in/out.

4) Quantify staleness behavior
- Measure observed stale duration across several runs (best/typical/worst).
- Explicitly report whether staleness appears to resolve within ~60 seconds.

5) Frame the unresolved product decision (do not decide it)
- Present impact tradeoffs for:
  - “<=60s staleness acceptable” vs
  - “near-real-time consistency required”
- Keep this as an open decision owned by product.

Deliverable format:
- Findings summary (1 short paragraph)
- Evidence log (timestamped bullets)
- Fault-domain assessment:
  - Cache: status + evidence
  - Indexer: status + evidence
  - Client: status + evidence
- Confidence level per conclusion (high/medium/low)
- Open questions / unknowns
- Recommended next steps (investigation or mitigation options), clearly separated from confirmed facts

Important:
- If evidence is insufficient to isolate a single root cause, provide the most likely ranked hypotheses and exactly what additional read-only checks would disambiguate them.
- Do not implement fixes.
```
