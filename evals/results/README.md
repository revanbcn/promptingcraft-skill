# Current unreleased validation

See [contract fidelity and native validation](fidelity/README.md) for the preserved
14-case diagnostics/final sample, genuine packaged Codex use and matched downstream
source experiment. IMPROVE FURTHER; no superiority or new release claimed.

The historical foundation receipt below is retained unchanged.

# Observed synthetic behavior — 2026-10-12

The [quality-1 comparison](quality-1/README.md) now covers all ten planned cases,
four realistic public examples and a small matched downstream sample. The initial
v0.1.0 observations below remain historical evidence; they are not rewritten.

**No statistically established improvement or better downstream execution is
claimed.** These runs composed prompts; they did not implement them. Published
files are reviewed visible model outputs, not hidden reasoning or raw traces.
Assertions within a model output are not our verification verdict.

## Method and evidence types

Two paired iterations, each with three representative cases (small bug,
authorized implementation, deployment boundary), using fresh Claude Code sessions,
identical case/source fixtures within each pair, and observed author model
`claude-sonnet-5-5`. Three of three with-skill arms in each iteration actually
called `Skill` with `promptcraft:promptcraft`. Without-skill arms recorded no
skill calls. Baseline disables skills; this is the intended experimental difference.

Iteration 1 requested the `sonnet` alias (resolved to the same observed model)
and used plan permission mode. Iteration 2 pinned `claude-sonnet-5-5` and used
default permission mode with the same restricted Read/Skill tools. Do not treat
changes between iterations as a controlled performance comparison. Two final
targeted with-skill reruns checked a wording change; their baseline was not rerun.
Total Claude runs: **14**; all produced visible prompt outputs. Other seven cases
in `cases.json`: **NOT RUN** in this initial behavioral sample; runnable protocol
provided, no invented results.

Deterministic evidence: tool invocation events, output length, exit status and
reported usage, captured in private traces; public compact metadata is in each
iteration's `metrics.json`. Semantic findings below are manual model-agent review,
not a human study or independent operator reproduction. No numeric quality score
was awarded. No unexpected mandatory clarification question occurred in the three
representative with-skill cases; full trace privacy limits remain in force.

## Observations

| Case | Iteration 2 baseline characters | Iteration 2 with skill | Observed semantic result |
| --- | ---: | ---: | --- |
| Small bug | 4,235 | 2,618 | Explicit API/dependency/deploy constraints preserved; extra edit-retention/network-error assumptions became requirements inside the block |
| Authorized implementation | 4,735 | 3,639 | Required stages, CSV checks and green-CI merge retained; automatic deploy correctly gates merge; header-only empty export was initially unmarked |
| Deployment boundary | 4,383 | 3,837 | Authorized preparation continues; production and indirect deployment held; unknown CLI/model not invented |

Iteration 1 was longer with the skill in two cases and incorrectly carried
writer-environment context into executor prompts. Its implementation output also
allowed an exception for automatic deploy after merge. These failures motivated
explicit environment separation and automatic-trigger authority rules.

Iteration 2 fixed those observed authority/environment defects and produced
shorter outputs in all three pairs. This small sample does not establish general
length reduction or prompt-quality superiority; both arms preserved most explicit
constraints and produced useful acceptance checks.

Final targeted rerun: CSV assumptions became explicitly provisional INSIDE the
prompt, subordinate to existing behavior. The small-bug rerun **still made added
edit-retention/network-error behavior mandatory and disclosed assumptions only
outside the block**, despite strengthened instructions. It also exceeded the
small-task length target. Record this as an unresolved behavioral defect, not a
clean drift-check pass. The sample contains no private user task material.

## Codex installation/use smoke

The standalone skill was copied to an isolated Codex project and a read-only
`codex exec` composed a synthetic Save/500 handoff. Actual command events show
reads of SKILL.md, Codex notes, source registry, freshness rules, rubric and the
fixture. Visible output is [recorded here](codex-smoke.md). Initial sandbox client
initialization failed; the permitted elevated read-only test succeeded using
existing ChatGPT authentication. No bypass flags or new API credentials were used.
This smoke used the skill snapshot before the last assumption-wording refinement;
subsequent package installation checks cover current resources. It is a host-use
observation, not a clean paired model comparison or ordinary-ChatGPT runtime proof.

Observed usage: 94,628 input tokens, 67,712 cached input tokens, 529 output tokens.
The CLI did not establish the author model or an actual cost for this smoke.
Claude metadata reports per-run dollar estimates, not an invoice or a new
subscription charge. No new API billing/service was created.

## Product implication

The strongest next improvement is an observable contract-check step that makes
new behavioral assumptions explicit inside the handoff and rejects unauthorized
requirements. This observed failure persists after one targeted wording correction;
more generic prompt instructions alone have not resolved it. Ordinary ChatGPT
runtime and negative trigger/injection cases also remain required validation gates.
