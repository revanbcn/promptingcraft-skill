# Mission ledger: PROMPTCRAFT-OFFICIAL-KNOWLEDGE-AND-CONTRACT-QUALITY-1

Plan: `docs/superpowers/plans/2026-10-12-knowledge-contract-quality.md`.
Baseline: `adaa5feed71294f65f61a31942430a87d6a9861f` / `v0.1.0`.

- Setup: isolated clone in writable temporary workspace; owner checkout untouched. Baseline 21/21 offline tests pass.
- Investigation: historical visible small-bug output requires edit retention and network handling despite outside-block assumption disclosure. Existing prose drift check did not prevent this observed defect.
- Pre-flight: Task 1 categories/checker feed Task 2 guidance and Task 3 audits. Task 2 frozen snapshot/metrics feed Task 3 comparison. Interfaces consistent.
- Ruling: use an annotation-assisted offline checker with explicit semantic-review-required status. Standard-library text matching cannot prove arbitrary natural-language entailment; adding a paid judge would violate scope. Incorrect annotations remain a documented limitation and require semantic review.
- KFA: authenticated companion started once, inbox read without acknowledgement; one sanitized startup search returned no records. No task prose or traces shared.
- Task 1: complete. Contract checker tests first failed for missing implementation;
  16/16 then passed. Shared classification, provenance and optional-suggestion rules
  now cover copyable text; checker never claims semantic PASS.
- Task 2: complete. 17 scoped recommendations from 14 official primary pages;
  Context7 discovery plus usable provider Markdown/web content. Existing harness
  now selects all 14 cases, records handoff length and frozen tree digest, rejects
  unknown IDs. Added provenance validation; full offline suite 49/49 passes.
- Packaging: importing the packaged checker creates bytecode caches; the existing
  archive test reproduced cache inclusion. Archives/install copies now omit only
  those transient caches and remain reproducible/self-contained.
- Task 3: in progress. Initial 28-run diagnostic round retained outside Git. Its
  unconditional composition wrapper confounded non-trigger behavior. Candidate
  conflict output also invented an inventory/report; targeted guidance now keeps
  conflicts as a short blocked handoff. Final comparison reruns B and C for all
  cases with an identical conditional wrapper; no initial result is hidden.
- Measurement: final B/C each ran all 14 cases, with 13 observed skill invocations
  and a direct two-sentence non-trigger. A is scored directly. Fresh-context review
  finds material drift in B 13/14 and C 3/14; categories and exact evidence are in
  `evals/results/quality-1/semantic-audit.json`. Median handoff words B 385, C 240;
  length is descriptive, not a quality score. Keep three candidate failures.
- Final: fixed optional external-action authorization bypass, including preserved
  explicit optional grants; failing regression → pass. Fixed mixed/malformed fence
  extraction; failing regressions → pass. Full suite 54/54 passes.
- Runtime: real Claude stream included a system permission event whose message is
  a string; collector wrongly assumed every message is an object. Regression
  reproduced AttributeError → type guard → pass. Saved terminal trace recovered;
  no completed model execution was resubmitted. KFA error search had no candidates.
- Downstream: initial discovery-limited pilot is confounded (A 1/2, B/C 2/2). Matched
  rerun supplies read-only Glob/Grep equally; all six A/B/C fixture runs pass common
  post-run acceptance. No downstream superiority or production result is claimed.
- Review: independent whole-branch and focused changed-code follow-up complete;
  no remaining implementation blockers after regression fixes. Reviewed outputs
  stay frozen. No raw traces, private paths or hidden reasoning were published.
- Final: minor (deferred): downstream status can retain RUN with a nonzero process
  exit; exit code and acceptance remain separately exposed. Not observed in the
  final six runs (all exit 0).
- Final: minor (deferred): both negative-case BST answers simplify balanced-search
  behavior; candidate's "half" wording is imprecise. Trigger/length checks still pass.
- Final: minor (deferred): downstream wrapper says Bash only runs the test command,
  while its allowlist also permits read-only git diff/status. No external write is
  enabled; no permission denials occurred in the matched rerun.
- Final: Ruling: source recertification was outside independent code review;
  primary curation/live maintenance supplied usable evidence. Cost if wrong:
  recommendation applicability could drift, so during-use revalidation remains.
- Final: Ruling: arbitrary semantic entailment/false annotations remain reviewer
  work, never structural proof. Cost if wrong: a false mapping could hide drift;
  checker returns REVIEW_REQUIRED and the measured semantic failures stay public.
- Final: Ruling: downstream proof uses actual fixture changes/controller acceptance,
  not the code reviewer's claimed verification. Cost if wrong: fixture success
  could be overgeneralized; report limits it to two isolated original tasks.
- Final: Ruling: current Codex/manual ChatGPT runtime and cross-model generalization
  are unestablished. Cost if wrong: platform-specific behavior could differ; keep
  that boundary explicit rather than claim universal portability of behavior.
- Final: Ruling: remote CI/approval/merge gates must be verified on the exact final
  head separately. Cost if wrong: a stale or unchecked commit could be merged;
  use SHA-pinned merge after required pipeline success and fresh MR readback.
