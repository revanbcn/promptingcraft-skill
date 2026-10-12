# PromptCraft new workflow and evidence review

Scope: the new instruction delta `9dfed6a..47bd098`, plus the fidelity evidence/docs publication. Previously reviewed code and resolved fixes were deliberately not reviewed again. No repository, index, HEAD or network mutations were performed. Private event inspection was restricted to tool/command/turn metadata; hidden reasoning and complete provider documents were not emitted or read as review content.

## New Important/Critical findings

None found in the new instruction delta or completed evidence review. Both documentation inaccuracies below were corrected and rechecked. The final execution audit was subsequently received and verified; see closeout below. No unresolved evidence-review blocker remains. This is not merge approval or CI readback.

## Documentation inaccuracies found and resolved

1. **Incorrect packaged-resource attribution.** `evals/results/fidelity/native/metrics.json:35` labels the live run's second command as reading packaged PromptCraft `SKILL.md`. The completed command in `native-elevated-events.jsonl` actually reads `<HOST_OPENAI_DOCS_SKILL_PATH_REDACTED>`, followed by PromptCraft's `freshness.md` and `rubric.md`. Remove `SKILL.md` from that command's `packaged_resources_read`, or represent the host documentation skill separately. Other packaged PromptCraft reference reads are genuinely observed, so this does not invalidate observed packaged resource use.
2. **Stale native-run count and snapshot wording.** `docs/fidelity-ledger.md:35-36` says two native invocations and calls the earlier no-change sample final-snapshot. Four completed native invocations now exist, with four distinct package/tree digests. Update to four and identify the final workflow sample separately, or label the two-run statement explicitly as historical. The result README and native metrics already distinguish the four correctly.

## Evidence checked directly

- All four ZIP SHA256 values in native metrics match their retained ZIP files. Recomputed skill-tree hashes inside those ZIPs match the four reported tree digests. Every extracted native installation file matches its corresponding ZIP entry byte-for-byte.
- The latest package/tree is `e448be4d31ae9390ca82ce926235d2d8e39c8d81efb0118175d98e1f1460c9b8` / `351b078a9c49e7a650a184a4504ccd2765a901217584d191e1787ebb2f812e40`. The final 14 composition metrics and 12 source-composition metrics use that same tree digest; the three diagnostics retain distinct earlier digests.
- Four native completed-turn records and their token-usage objects match the published native metrics. The observed commands read packaged resources, and the no-change/delivery/final cases read their task text. No task edits or tests appear in these native command observations.
- The live native trace contains completed Context7 resolve/query calls and actual web open/find events. The other three native traces have no such retrieval events, consistent with their dated-cache labels. The documentation makes no native model or cost claim.
- All 12 final B/C source traces contain successful reads of the exact expected fixture path. The fixture bytes hash to the corresponding per-arm recorded digest. The normalized private source file's SHA256 and 32,389 character length match `guidance-fetch.json`; only the digest/length were inspected, not its prose. This supports matching supplied evidence, not a claim of author-side live retrieval or comprehension.
- The B/C already-suitable outputs both select no-change and echo the original task. Both necessary-correction outputs identify the conflicting deployment instructions and retain a deployment hold, rather than claiming no revision is needed.
- Published diagnostic counts reconcile to the audits: same historical outputs newly judged 5/14 versus retained historical 3/14; diagnostic candidate counts 3/14, 1/14, 3/14; final 0/14. Published final and diagnostic-2/3 per-row judgments match the respective private blind-review records, with added case mapping only. The final audit covers all 14 cases and expressly limits readiness to prompt usability.
- Final execution command traces contain exactly the two disclosed read-only A discovery-command violations: `cat README.md manifest.json; ls` and `ls -R . && cat README.md billing_dialog.py profile_dialog.py`. All three manifest arms attempt the exact unittest command once; discussion/dialog traces contain no test commands. Published counts separate host-command restrictions from task edit/test authority.
- Recomputed final execution cost/time aggregates match the README: A $0.040517 / 28.07 s; B $0.061431 / 33.81 s; C $0.055921 / 31.08 s. B/C six-case composition costs separately match $0.435767 / $0.426943.
- The new workflow prioritizes original-prompt critique and narrowly sourced corrections. The later existing no-change conditions still exclude contradictions, unsupported authority and blocking unresolved decisions. The new wording does not itself authorize implementation or make source freshness an effectiveness claim.

## Declined-to-judge boundaries

- Final downstream blind judgments were subsequently published and checked, as recorded below. Their declared input limits remain: the blind reviewer received observation summaries/diffs and visible outputs, not raw executor traces. This evidence review separately inspected raw tool metadata; it does not turn model judgments into independent human calibration.
- The native events do not export a Skill activation event or the original launch arguments. They establish actual packaged resource consumption and completed turns; explicit invocation is documented by the controller rather than independently reproduced from a native activation event. The publication correctly disclaims exported activation telemetry.
- Historical retrieval date/raw response byte size and source applicability beyond the supplied paraphrase were not independently re-fetched. The stored normalized hash/length were checked. Fresh evidence does not establish superiority.
- No independent human calibration, statistical improvement, production outcome or cross-operator replication is established. Iterative diagnostic variance is retained rather than pooled into a success claim.
- The 85-test RED→GREEN fix history and current tests were not rerun in this evidence-only review, per the instruction not to duplicate resolved fix review. Their gate belongs to the executor's recorded checks and final CI.
- Remote CI, final SHA acceptance, MR/merge readback, release assets and authorization flags were not reverified. Those remain separate gates. No release/deploy authority is inferred.

## Final execution audit and closeout

`evals/results/fidelity/final-execution-audit.json` is now present. Removing only the post-scoring `case` and `arm` mapping fields yields execution judgments identical to `/private/tmp/promptcraft-fidelity/blind-guarded-execution-review.json`; its four composition judgments also match exactly. All nine case/arm cells occur once. Per-cell host-command counts and controller records match final execution metrics.

The actual audit contains six COMPLETE outcomes (three manifest repairs and three discussion proposals) and three CORRECTLY_BLOCKED dialog outcomes. The two host-command violations are recorded on A, distinct from zero recorded task-scope violations. Clarification requests are explicitly counted: dialog A/B/C each ask three questions, of which two/two/three are blocking. These extra questions are not hidden by the successful target hold. Three manifest arms each have one observed successful executor verification and a distinct one-test passing controller record; discussion/dialog verification is not applicable. The published outcome table is consistent with these judgments.

Both already-suitable final B/C copyable blocks were also compared directly with `task_prompt` in the predeclared cases and are exactly equal. This closes the unchanged-text limitation of the blind composition reviewer, whose package did not include the complete originals. Both correction outputs preserve a deploy hold and identify the source conflict.

The corrected native metric no longer counts global OpenAI documentation `SKILL.md` as a packaged PromptCraft read. The mission ledger now states four distinct ZIP snapshots and names the final workflow sample separately. Both documentation findings are resolved.

**Final evidence verdict:** no new Critical/Important finding and no unresolved documentation inaccuracy identified in this scoped pass. Evidence supports the narrow, explicitly qualified publication. Required final-SHA CI and authorized MR/merge readback remain the coordinator's separate gates; no release or deployment claim follows.
