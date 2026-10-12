# PromptCraft contract fidelity: code review

Reviewed base `135a527dbfe3f4b1fb9b9f95a252ada3dd7dc335` through head `9dfed6a` read-only. This covers core instructions, optional checker, evaluation collectors, fixtures, tests and documentation. Results/native evidence publication is outside this reviewed diff.

**Recommendation: resolve the three Important findings before the merge gate.** No Critical findings. Existing 78 offline tests pass, including packaging tests; the reproductions below also ran locally without model calls. No repository files, index or HEAD were changed.

## Important

### I1. A rejected no-change phrase silently restores a contradictory original as the handoff

Location: `scripts/evaluate.py:73-80` (especially marker membership at line 73 and fallback at lines 77-80).

`parse_events` recognizes the marker anywhere in whitespace-normalized prose, without requiring it to be the actual outcome declaration. A response such as:

> Do not use the no-change response "The original prompt is already suitable. No material revision is necessary." here: the deployment clauses conflict. Ask the owner to resolve them.

is parsed as `composition_outcome=UNCHANGED`. Given original `Deployment is forbidden. After tests pass, deploy immediately.`, the collector synthesizes exactly that conflicting text as `handoff`, despite the author explicitly requiring a correction. The execution harness subsequently consumes this handoff. This violates the necessary-correction requirement and misrepresents the model's decision, rather than merely lacking semantic grading.

Require an unambiguous declaration protocol or a narrowly anchored standalone outcome, with ambiguous/quoted/negated mentions left unresolved. Add a regression for this actual negative response, alongside the legitimate declaration-only and exact-echo cases. Also retain raw fenced content for byte identity: `extract_handoff` strips whitespace, so an altered echo with added leading spaces can pass identity, while an exact original with meaningful leading spaces can fail it.

### I2. Unauthorized-action metrics omit Bash attempts except one exact test command

Location: `scripts/evaluate_fidelity.py:81-93`.

The collector counts Edit/Write for discussion/ambiguous cases and the exact `VERIFY` command for discussion. Other Bash actions are silently counted as zero unauthorized attempts. Reproduced examples:

- `discussion-only`: `python3 -m unittest` → unauthorized_action_attempts=0, verification_attempts=0, despite the explicit prohibition on tests.
- `manifest-command`: `git commit -am fix` → unauthorized_action_attempts=0, despite the explicit prohibition on commits.
- `ambiguous-dialog`: `rm profile_dialog.py` → unauthorized_action_attempts=0, despite target resolution being required before changes.

These are relevant even when the tool rejects them: attempted unauthorized actions are an explicit evaluation dimension, and the existing test already establishes that denied attempts should count. A narrow permission allowlist protects execution but does not make a zero attempt count truthful.

Classify Bash attempts against each case's authority, including denied calls. Where shell semantics cannot be classified safely, emit an explicit unclassified/review-required count rather than a definitive zero. Test alternate test commands, denied commit/deploy/write attempts and ordinary allowed read commands. Keep attempted, allowed and successful actions separate.

### I3. The exact immutable policy can match an unrelated field while the active policy changes bytes

Location: `scripts/evaluate_fidelity.py:58-59`.

`POLICY in text` is a file-wide substring test; the active `policy` is compared only as a parsed Python object. The following changes pass with no findings after the verify typo is repaired:

```json
"unchanged_example": {"schema":1,"fields":["job_id","status"],"terminal":"failed_final"},
"policy": {"schema": 1, "fields": ["job_id", "status"], "terminal": "failed_final"}
```

The active policy has been reformatted, contrary to the fixture's explicit exact-span invariant. The unrelated field supplies the expected bytes. The duplicate-key defense does not catch this because the keys differ. This produces a false deterministic artifact pass for the central immutable-text requirement.

Bind the exact-byte check to the active top-level policy value (or validate an allowed edit against the original manifest, permitting the verify repair and legitimate unrelated whitespace while preserving that specific span). Add a regression with a separate decoy copy and a changed active policy. Do not fix this by freezing the entire manifest: that would recreate the contract defect being repaired.

## Minor

### M1. Relative output paths make the frozen plugin path relative to the wrong working directory

Location: `scripts/evaluate_fidelity.py:121-125,143-145`.

The CLI accepts relative `--output`, but passes `output/skill-snapshot` directly to `--plugin-dir` after setting the child cwd to `output/<case>/<arm>/work`. A relative plugin path is therefore resolved below that nested work directory, not the caller's directory. Documentation examples use absolute paths, so the documented path works; other valid CLI inputs can lose skill activation or fail cells. Resolve the output/frozen path before constructing child arguments and add a no-model subprocess-argument test.

### M2. Manifest artifact checks do not detect removal of the existing test suite

Location: `scripts/evaluate_fidelity.py:38-64`.

Repairing the command and emptying `tests/test_contract.py` yields no artifact findings. A subsequent unittest discovery may report success with zero tests. `changed_files` and blind semantic review can still expose this, so this is not graded as an unqualified completion claim; however, the deterministic evidence does not establish that the repaired command runs the existing suite. Preserve the original fixture test hash or run independent controller-owned acceptance and record the test count. This is an evaluation-fixture invariant, not a general restriction on task authors editing tests.

## Positive checks

- Core instruction changes preserve immutable spans, discussion mode, unresolved scope choices, authority strength and planning freedom; they explicitly reject the three diagnosed transformations and invented API exceptions/host authority replacement.
- No-change retains contract critique and explicitly requires necessary corrections. I1 is in collection, not the text instruction.
- The checker adds exact presence, local-action provenance and identity checks without claiming semantic entailment. Missing annotations, contradictory prose and extraction completeness remain explicitly review-required.
- Frozen plugin snapshots, fresh fixtures, retained partial timeout output and unknown exits are present. Tool success is distinguished from attempts in the supported categories.
- `evals/cases.json` and the original 14-case definitions are unchanged in this diff. Existing test assertions were retained; additions are additive.
- Attribution remains present. Release version metadata and release/tag workflows were not changed by this diff.

## Declined to judge / required evidence boundaries

1. **Native Codex activation, actual ZIP installation, draft/critique/final/source behavior and ChatGPT availability.** The ledger asserts observations, but the underlying native evidence/results publication is explicitly a later diff. These remain unreviewed here, not disproven.
2. **Actual blind scoring, anonymization, adjudication, per-arm completion/clarification/cost outcomes and comparative superiority.** No outcome superiority follows from code inspection or 78 passing tests. Those need the supplied blind artifacts and scoring evidence.
3. **Historical external retrieval and applicability of the C summary.** The supplied file provides attribution/date/hash, but this review did not replay the historical source retrieval. Source freshness is not effectiveness. Successful Read counters alone establish neither the content consumed nor comprehension; publication should check the actual matching file/path and successful trace evidence.
4. **Matched-run eligibility when source reads, skill activation or model identity are absent.** The runner records these fields but does not reject such cells automatically. A final report must exclude or explicitly label unmatched/diagnostic cells. It must not convert the metadata's presence into a successful matched experiment.
5. **Semantic completeness of reviewer-authored annotations.** The checker explicitly disclaims it; this is an appropriate boundary, not a hidden automatic safety guarantee.
6. **Remote CI, MR status, release asset immutability and merge authorization readback.** No network writes or remote state verification were performed. Existing release metadata is unchanged locally; external release assets were not reverified.

## Validation performed

- Read complete core/harness diff, new fixtures, acceptance tests, plan and ledger.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`: **78 passed**.
- Ran isolated temporary-directory reproductions for I1, I2, I3 and M2; each produced the behavior described above.
- Git status was clean during the main review. The author then supplied a concurrent narrow defect-intent patch; it was inspected separately below. This reviewer made no model/CLI execution calls, repository writes, index changes, HEAD changes or network writes.

## Addendum: supplied defect-intent wording

Also inspected the subsequent uncommitted additions in `skills/promptcraft/SKILL.md:35-39` and `skills/promptcraft/references/contract.md:16-18`: user-reported defects remain task intent, are labeled user-reported when appropriate, and should be reproduced rather than replaced by the current faulty behavior. This is consistent with the source-contract boundary and adds no new finding. The original 78-test run predates this concurrent patch.
