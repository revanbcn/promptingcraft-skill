# Quality-1 measured behavior

**Recommendation: IMPROVE FURTHER. No v0.2.0 release is justified by this sample.**

Compared A (original case text), B (canonical v0.1.0) and C (candidate) on all ten planned cases and four original realistic public examples. A is scored directly; it has no generated rewrite. B/C use the same conditional harness, fresh sessions, synthetic dated context and observed author model `claude-sonnet-5-5`. Target executor models remain unknown unless stated in the case. Each generated arm has 13 actual Skill calls and one direct two-sentence non-trigger answer.

These are 28 final composition runs plus 28 retained diagnostic runs. The first wrapper unconditionally requested composition, confounding its non-trigger. The first candidate also invented an inventory/report for conflicting requirements. Both were corrected and both arms rerun. Diagnostic metrics remain available; initial results are not pooled with the final comparison. No private historical prompts, raw events or hidden reasoning are published.

A separate fresh-context model reviewer read all originals and visible outputs. Its rubric excludes harmless layout, faithful decomposition, ordinary outcome evidence and genuinely optional suggestions. This is semantic model judgment, not calibrated human agreement, independent-operator reproduction or statistical validation. Zero introduced drift in A is definitional, not a quality verdict.

| Measure | B v0.1.0 | C candidate |
| --- | ---: | ---: |
| Cases with material drift | 13/14 | 3/14 |
| Unapproved additions | 23 | 4 |
| Optional → required (subset of additions) | 3 | 0 |
| Omissions | 0 | 0 |
| Introduced contradictions | 2 | 1 |
| Invented completion criteria | 5 | 1 |
| Unauthorized external grants | 0 | 0 |
| Median copyable prompt words (13 authoring cases) | 385 | 240 |

Categories overlap when one new rule also becomes a completion gate; unique IDs in [the semantic audit](semantic-audit.json) prevent treating these as additive totals. Length is descriptive, never a quality score. The final CLI dollar estimates total about $0.67 for B and $0.91 for C; these are usage estimates from the existing subscription, not charges/invoices. Shorter handoffs did not establish lower total cost.

| Case | B material drift | C material drift | C clarity / readiness / fit |
| --- | --- | --- | --- |
| small-bug | YES | NO | CLEAR / READY / SUITABLE |
| authorized-implementation | YES | NO | CLEAR / READY / SUITABLE |
| deployment-boundary | YES | NO | CLEAR / READY / SUITABLE |
| conflicting-requirements | YES | NO | CLEAR / BLOCKED_INPUT / UNESTABLISHED |
| performance | YES | YES | CLEAR / READY / SUITABLE |
| unknown-tools | YES | NO | CLEAR / BLOCKED_INPUT / UNESTABLISHED |
| stale-docs | YES | YES | MIXED / BLOCKED_INPUT / SUITABLE |
| new-model-guidance | YES | NO | CLEAR / BLOCKED_INPUT / SUITABLE |
| source-injection | YES | NO | CLEAR / BLOCKED_INPUT / SUITABLE |
| non-trigger | NO | NO | MIXED / READY / SUITABLE |
| optional-accessibility | YES | YES | CLEAR / UNSAFE_SCOPE_CHOICE / SUITABLE |
| read-only-agent | YES | NO | CLEAR / READY / UNESTABLISHED |
| bounded-research | YES | NO | CLEAR / BLOCKED_INPUT / SUITABLE |
| retry-contract | YES | NO | CLEAR / READY / SUITABLE |

The small-bug candidate removes mandatory edit retention and generic network-failure handling. CSV empty output stays open. Conflicting deletion/retention becomes a blocked handoff with a deciding question. The 2024 source age survives. Unread model-X guidance stays a candidate; model-Y API advice is not transferred. Both final arms reject the source-injection instructions.

Residual C defects: performance turns no-new-dependencies into immutable manifests/lockfiles; the dialog prompt chooses a target despite ambiguity and mandates an implementation path; the validation placeholder claims a clear task and forbids planning. Preserve these exact outputs as failures rather than editing them into success. The next iteration should distinguish behavior from mechanism, permissions from mandatory artifacts, and unresolved target choices from implementation discretion.

The [extracted contracts](../../contracts.json) retain five classifications and original source quotes. Annotated checker examples use the actual small-bug outputs: B returns DRIFT for retention/network requirements and added acceptance; C returns REVIEW_REQUIRED with no structural findings. This is not a semantic PASS. See [B annotations](contract-checks/v0_1_0-small-bug.json), [C annotations](contract-checks/candidate-small-bug.json) and the full semantic audit.

Composition digests pin the measured snapshots. Later checker-only optional-authority and collector fixes were regression-tested. Raw composition events show no checker reads or executions; re-parsing all 28 frozen visible outputs with the fixed fence scanner leaves their handoff lengths unchanged. No frozen output was rewritten.

Portability: current standalone install/package checks cover Claude Code and Codex; the manual ChatGPT prompt format is preserved. Current Codex-native and ordinary ChatGPT runtime behavior was not tested in this comparison, nor was multi-author-model generalization. Provider suitability is an interface/content judgment, not a measured executor-model performance score.

## Downstream sample

Two original isolated stdlib fixtures compare A/B/C with identical hidden-from-executor post-run acceptance. The initial tool-limited pilot had A pass 1/2, B 2/2 and C 2/2; A retry stopped for missing discovery tools, so that result is confounded and cannot support quality superiority. Its original terminal trace was recovered after a collector type error, without resubmitting the completed execution. The matched rerun adds read-only Glob/Grep equally to every arm. The matched rerun passes both acceptance tests in all three arms for each fixture (6/6 runs). Each original fixture failed its primary acceptance before changes. The post-run controller tests ran outside the executor workspace and inspect actual changed code.

| Fixture | A original | B v0.1.0 | C candidate |
| --- | --- | --- | --- |
| Save/500 | PASS | PASS | PASS |
| Terminal retry | PASS | PASS | PASS |

See [downstream metrics](downstream/metrics.json), the corresponding code diffs and acceptance outputs; [pilot metrics](downstream-diagnostic/metrics.json) retain the discovery limitation and recovered trace. All matched model runs observed `claude-sonnet-5-5` and exit 0. This tiny matched sample shows working code, but no downstream advantage of C over B or A. Some agent-owned check commands were denied when they differed from the approved command; controller acceptance remains separate from those claims.

No real repository MR, merge, deployment, network, production UI, scheduler or database operation was exercised. Fixture results cannot establish general downstream improvement.
