# Behavioral evaluation

`cases.json` has ten original synthetic cases: small bug, authorized implementation,
performance, conflict, unauthorized deployment, unknown tools/model, stale docs,
new model guidance, source injection and a non-trigger. No historical user prompts
or conversations are included. `fixtures/guidance.md` is authored test data, never
claimed as live official guidance. Four additional original realistic public
examples cover optional accessibility work, a read-only agent investigation,
bounded manual research and a worker retry fix. They are representative scenarios,
not private production prompts or a sample of actual user traffic.

Optional paired run using an existing authenticated Claude Code subscription:

```sh
python3 scripts/evaluate.py --output /tmp/promptingcraft-evals --model claude-sonnet-5-5
```

The default now runs ALL cases; `--cases` selects an explicit subset and rejects
unknown IDs. Each arm starts a fresh temp
workspace with identical task/source fixture and Read/Skill tool allowance.
With-skill loads the session plugin; without-skill disables skills. Global setting
sources and MCP servers are excluded; no Bash, edit, deploy or external-send tools
are allowed. The executor's target model can remain unknown even when the prompt
author's model is observed. Pin a resolved model ID for repeat comparisons.

Raw traces stay outside Git. Before publishing synthetic prompt outputs, review
for leaked paths, account/session details, private content and hidden reasoning;
publish final visible outputs and compact observed metrics only. Report model ID,
actual skill invocation, constraints lost, acceptance checks, unnecessary questions,
output length, wall time and token/cost data when available. A CLI-reported dollar
estimate is not evidence of a new bill or actual subscription charge.

Classify results separately: deterministic package checks; model-judged/manual
semantic observations; observed host behavior. Self-review is not independent
verification. Three cases don't establish general improvement or better downstream
execution. These tests compose handoffs, not implement fixes in a target repository.
See [recorded results](results/README.md) and [surface status](../docs/verification.md).

## Three-way quality comparison

A is the original case text, scored directly rather than rewritten by another
engine. B is the exact v0.1.0 skill tree at `adaa5feed71294f65f61a31942430a87d6a9861f`.
C is the candidate. Use one shared case file/harness, pin the author model, use
fresh output folders, and freeze both skill trees during the run:

```sh
python3 scripts/evaluate.py --output /tmp/quality-baseline --arms with_skill --model claude-sonnet-5-5 --skill-root /path/to/v0.1.0
python3 scripts/evaluate.py --output /tmp/quality-candidate --arms with_skill --model claude-sonnet-5-5
```

The harness instructions are conditional: non-authoring requests get a normal
answer. An unconditional "composition only" wrapper confounds the negative trigger
case. Results from that initial wrapper are diagnostic, not the final comparison.
Record actual Skill invocation, observed model, source-tree digest, elapsed time,
token metadata and visible output. Measure the copyable handoff separately from
the entire response. Multiple/missing blocks are unresolved, not silently chosen.

For each case compare the original contract with every final operative clause.
Count material unapproved additions (including optional strengthening), omissions
and introduced contradictions, with short quoted evidence. Do not count formatting,
faithful decomposition, ordinary result evidence or clearly optional ideas as drift.
Separately assess clarity, readiness given missing inputs, provider/interface fit,
source freshness and trigger behavior. Preserve unknowns, and publish the rubric
and per-case judgments instead of claiming independent human validation.

The optional offline contract checker validates annotated source provenance and
coverage. Its clean result is REVIEW_REQUIRED; semantic review remains required.
Do not require the composing model to execute Python when its tools exclude Bash.

## Small downstream sample

```sh
python3 scripts/evaluate_downstream.py --output /tmp/quality-execution --baseline /tmp/quality-baseline --candidate /tmp/quality-candidate
```

This runs the original task, B and C on two original isolated stdlib fixtures
(Save/500 and terminal retry), with identical post-run acceptance tests outside
the executor's workspace. Only the original task's composition prefix is removed;
all arms get the same local-only host boundary. Restricted Claude file tools stay
within its working directory; approved Bash commands run local checks/diff only.
No real MR, network, merge, deploy or database operation is measured. Record the
initial failing acceptance, actual changed code and final acceptance separately
from the agent's claims. Six successful fixture runs would still not demonstrate
general downstream superiority or a real production outcome.

## Contract fidelity experiment

`fidelity-cases.json` adds six original cases without replacing the 14 existing
cases: repair a manifest command while preserving an exact policy, discussion
without implementation, unresolved dialog target, immutable manifest/order,
already-suitable no-change, and a necessary authority correction.

```sh
python3 scripts/evaluate_fidelity.py compose --output /tmp/fidelity-compose
python3 scripts/evaluate_fidelity.py execute --output /tmp/fidelity-execute --compositions /tmp/fidelity-compose
```

A is the exact task body. B/C load the same frozen skill/plugin and use the same
observed author/executor model, tools, workspace fixtures and host boundary. B has
synthetic dated context; C has a short attributed official summary externally
verified on the stated date. Both must read the source file; successful Read events
are recorded. This is supplied verified evidence, not live author retrieval or
model-specific tuning. Source metadata stays outside executor handoffs.

Execution exposes identical local file tools even for discussion tasks, so write
or test attempts without task authority can be measured. Source fixtures are
copied afresh for each cell; source-only guidance files are not execution inputs.
Arm order rotates across tasks. JSON/byte/hash acceptance checks run outside the
executor. Blinded model review assesses proposals, scope choices, clarification,
verification and completion; artifact pass alone cannot establish those outcomes.
Tool success reports, controller acceptance and executor assertions remain distinct.
Clarification for an unresolved target is the correct response, not a failed fix.

Collectors retain partial timeout traces, unknown exits and ERROR/TIMEOUT states;
they do not retry completed or uncertain model executions. A reported no-change
reuses the exact original task; an echoed block must match it. Missing or competing
blocks stay unresolved. Publication includes reviewed visible outputs and compact
metrics only. Raw events, private workspace paths and blind mappings stay private.

The earlier two tasks saturated because the bugs and acceptance checks were small,
local and explicit, and original prompts already gave adequate instructions. The
new cases test authority, exact bytes, ambiguity and verification as well as edits.
They can reveal differences; they do not guarantee a winning arm. One cell per arm
cannot establish general superiority, causal source effects or production value.
