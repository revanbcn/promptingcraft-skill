# Official knowledge and contract quality implementation plan

> **For agentic workers:** Use superpowers:executing-plans for native execution, then one fresh-context branch review. Steps use checkbox tracking.

**Goal:** Ground Promptcraft in current official guidance while preserving user requirements.
**Architecture:** One shared, source-anchored contract with conditional provider guidance. An offline annotation-assisted checker verifies provenance and coverage; semantic judgments remain visible and reviewable, never a claimed semantic proof.
**Tech stack:** Existing Python 3.11+ standard library, portable Markdown/JSON skill, GitLab CI, existing Claude Code subscription.
**Spec:** Owner mission PROMPTCRAFT-OFFICIAL-KNOWLEDGE-AND-CONTRACT-QUALITY-1; summarized in the global constraints below.

## Global constraints

- Canonical baseline: v0.1.0 at adaa5feed71294f65f61a31942430a87d6a9861f. Do not call it behaviorally validated.
- Preserve goals, required constraints, exclusions, scope and authority. Optional/inferred/unresolved material cannot become mandatory without original authorization.
- Classify EXPLICIT_REQUIRED, EXPLICIT_OPTIONAL, INFERRED, UNRESOLVED, FORBIDDEN. Suggestions are visibly optional inside the handoff.
- Curate current official OpenAI/Anthropic guidance with URL/title/date/scope/recommendation/limits/applicability/conflicts; distinguish official provenance, model scope, inference and experimentation.
- Run all 10 planned cases plus four original realistic public examples. Compare original input, v0.1.0 and candidate with identical composition harness/model, then a small downstream sample if practical.
- No new paid APIs/services. No release/version/tag change. MR and merge authorized only after checks and review. No deployment.
- Retain Claude Code, standalone Codex and manual ChatGPT; one contract core. Preserve private raw traces outside Git.

## Review focus

- False provenance: a cited goal must not justify unrelated features or acceptance thresholds.
- Optional laundering: an outside-block note must not excuse an imperative inside the handoff.
- Partial annotation, missing exclusions, opposite polarity and unapproved external actions fail closed.
- Faithful decomposition/formatting must remain allowed; semantic interpretation is not a deterministic proof.
- Evaluation artifacts must distinguish observations from self-claims, length from quality, and isolated execution from real production proof.

### Task 1: Contract checker and shared skill behavior

**Files:** Create `skills/promptcraft/scripts/contract_check.py`, `tests/test_contract.py`; modify `SKILL.md`, `references/contract.md`, `references/rubric.md`, `references/examples.md`.
**Interfaces:** Produce `check(document: dict) -> dict` and CLI JSON input/output. Original source spans, classified requirements and ordered final clauses are the common input.

- [ ] Write tests for new requirements, optional strengthening, omissions, contradictions, actions, invented completion criteria, faithful decomposition, partial annotation and bad provenance.
- [ ] Run `python3 -m unittest discover -s tests -p test_contract.py -v`. Expected: failure before implementation.
- [ ] Implement the smallest stdlib checker and guide; make mandatory clauses traceable, omit unnecessary inferred preferences, leave unresolved conflicts unresolved.
- [ ] Run the same tests. Expected: pass, with semantic-review-required status on structurally clean documents.

### Task 2: Curated knowledge and evaluation harness

**Files:** Create `references/knowledge.json`, `tests/test_evaluate.py`; modify provider notes, registry, validation, `scripts/evaluate.py`, `evals/cases.json` and evaluation protocol.
**Interfaces:** Consume shared contract categories; produce scoped recommendations and `run(..., skill_root=None, cases_file=None)` for frozen baseline/candidate comparison.

- [ ] Fetch current documentation using Context7 and official primary pages. Record evidence and limits; preserve conditional recommendations.
- [ ] Test all-case selection, rejected unknown IDs, frozen skill roots, trace/model metrics and exact handoff extraction; run before implementing. Expected: failures for missing behavior.
- [ ] Extend existing harness without adding services; preserve fresh workspaces and restricted composition tools.
- [ ] Run full offline suite, validator and package builder. Expected: all pass.

### Task 3: Measure, review and deliver

**Files:** `evals/results/quality-1/`, results/protocol docs, README, changelog and mission ledger.
**Interfaces:** Consume exact baseline/candidate snapshots and original cases; publish reviewed visible outputs and compact per-case measurements only.

- [ ] Run baseline/candidate for all cases with the same pinned model and harness. Record non-invocations/errors without silently treating them as passes.
- [ ] Review all outputs against original requirements; record additions, omissions, contradictions, clarity/readiness/suitability and prompt length. A has no generated rewrite; score the original directly.
- [ ] Run a bounded isolated downstream sample if feasible; use identical test fixtures and acceptance checks for all arms.
- [ ] Complete one independent fresh-context code review; fix important defects and run affected/full checks.
- [ ] Open MR; verify exact head CI, approval/discussion gates and absence of deploy triggers; merge only when gates pass.
- [ ] Record post-merge main pipeline and preserve v0.1.0 release. Recommend RELEASE / IMPROVE FURTHER / HOLD from measured behavior.
