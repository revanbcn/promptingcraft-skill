# Agent Skills standard audit — PromptingCraft.com skill 0.2.0

Audited 2026-10-12 against the official Agent Skills documentation
(https://agentskills.io/llms.txt: specification, optimizing skill descriptions,
evaluating skills, using scripts, best practices) and the `skills-ref` reference
validator (agentskills/agentskills, commit `69ef37e`). Native runs used Codex CLI
0.162.1 with the configured model `gpt-6.1-sol` (reasoning `xhigh`) and the installed
local plugin `promptcraft@dondego-local` 0.2.0, whose skill is byte-identical to
`skills/promptcraft`. All runs were made by the same operator; none is an independent
reproduction.

The native runs used the skill before this audit added the agentskills.io entries
to `references/sources.json`. That change only adds registry rows that apply to
authoring Agent Skills; `SKILL.md` and every other skill file are unchanged.

## Verdict

The skill complies with the specification. Activation is reliable in Codex on the
tested set and the description needs no change. No genuine instruction defect was
found that justifies rewriting the skill, so `SKILL.md` is unchanged. The changes in
this audit are evaluation assets, a separately classified standards source and the
recorded results.

## Specification compliance

| Requirement | Result |
| --- | --- |
| `skills-ref validate` on `skills/promptcraft`, the skill ZIP and the plugin ZIP | Valid skill (all three) |
| `name`: 1–64, lowercase/digits/hyphens, matches directory | `promptcraft` |
| `description`: 1–1024, says what and when | 247 characters; states the task and the trigger boundary |
| `license`, `metadata` (string to string) | `MIT`; `author`, `website`, `version: "0.2.0"` are strings |
| `compatibility`, `allowed-tools` | Absent: no special environment and no pre-approved tools are needed |
| Body under 500 lines and about 5,000 tokens | 212 lines, 1,908 words (about 3,400 tokens) |
| Progressive disclosure | References load on demand by step; `knowledge.json` is read per relevant record |
| File references relative and one level deep | All links resolve inside the skill; reference files link nothing further |
| Scripts self-contained with clear errors | `scripts/contract_check.py` uses only the Python standard library; optional |
| Installation paths | Plugin `skills/promptcraft/`; standalone `.agents/skills/promptcraft` (Codex) and `.claude/skills/promptcraft` (Claude Code) by `scripts/install_skill.py`, unit-tested |

Client compatibility: Codex native loading is observed (below). The Claude Code
install path is covered by the isolated-install unit test, but this audit did not run
Claude Code natively. ChatGPT is not verified (see **ChatGPT limits**).

## Activation (description optimization method)

`evals/trigger/queries.json` holds 20 realistic queries: 10 should-trigger (formal,
casual, terse and context-heavy, explicit and implicit) and 10 near-miss
should-not-trigger queries (coding tasks, prompt writing for other purposes,
questions about Codex or prompt injection). They are split into a fixed train set
(12) and a held-out validation set (8), each half positive. Each query ran 3 times in
a fresh empty directory with `scripts/evaluate_triggers.py`. A run counts as
triggered only when the host actually read the installed `SKILL.md` from the plugin
cache; the model's own claims are ignored.

| Set | Pass | Positive runs triggered | Negative runs triggered |
| --- | --- | --- | --- |
| Train | 12/12 | 18/18 | 0/18 |
| Validation (held out) | 8/8 | 12/12 | 0/12 |
| Total | 20/20 | 30/30 | 0/30 |

Five attempts failed on the host side (three transport errors, two capacity responses)
and were retried, leaving 60 valid runs; see `evals/results/trigger-1/`. Because every train query already passes, there is
nothing to optimize, and editing the description would only risk overfitting. The
description is kept.

## Reviewer cases (behavior)

`evals/review/cases.json` (7 positive, 4 negative) ran natively; outputs are in
`evals/results/review-native/`.

| Case | Skill loaded | Observed outcome |
| --- | --- | --- |
| P1 explicit Codex task | yes | No-change with the task echoed exactly; freshness labeled |
| P2 multi-turn, natural language | turn 1 no, turn 2 yes | Turn 1 acknowledges only; turn 2 keeps `id,name,status`, existing action, no dependencies, implementation yes / deployment no |
| P3 review a Claude Code prompt | yes | Keeps all four requested tasks (the user said not to change scope), the formatDate invariant, removes the duplicated caution |
| P4 no-change | yes | Exact no-change sentence and unchanged body |
| P5 unresolved repository | yes | Neither repository chosen; asks first; investigation only, no edits |
| P6 official guidance, keep intent | yes | No-change; guidance link and date given (first attempt timed out at 900 s, re-run 82 s) |
| P7 Cursor agent task, natural language (added later) | yes | No-change with the task echoed exactly; links Cursor's Agent prompting guide; no freshness date label was given |
| N1 unrelated question | no | Two-sentence answer |
| N2 software topic, not a prompt request | no | Explanation only |
| N3 run a production migration now | yes (explicit invocation) | States nothing was run or pushed; prompt keeps the user's own authorization, leaves repository and database unresolved, asks which to target |
| N4 birthday message | no | Message only |

The P1 and P3 expectations were revised after the run, and the revision is recorded
in the case text: P1's no-change outcome is permitted by `SKILL.md`, and P3's first
expectation contradicted the user's explicit "without changing its scope".

## With and without PromptingCraft.com

Five single-turn requests ran twice with the plugin enabled and twice with it
disabled (`-c plugins.promptcraft@dondego-local.enabled=false`; no `SKILL.md` read was
observed in any disabled run). A fresh grader (Claude Sonnet 5.5, one pass) saw the 20
outputs under seeded shuffled labels and graded each against its stated contract and for
added mandatory requirements. Data, grader prompt and per-item verdicts:
`evals/results/ab-1/`; runner: `scripts/evaluate_ab.py`.

| Case | With: pass, defects | Without: pass, defects |
| --- | --- | --- |
| Review a prompt, keep scope | 2/2, 0 | 0/2, 5 |
| No-change | 2/2, 0 | 2/2, 0 |
| Unresolved repository | 2/2, 0 | 0/2, 5 |
| Delegate CSV fix | 0/2, 3 | 1/2, 2 |
| Drop Python 3.9 in two files | 2/2, 0 | 0/2, 4 |
| **Total** | **8/10, 3** | **3/10, 16** |

These figures exclude one contract item that contradicted the user's request; the raw
grades, before that exclusion, were with 6/10 and 5 defects, without 3/10 and 18
defects. Without the skill, the model most often added mandatory gates, procedures or
assumed values (for example, a `python_requires >=3.10` the user never chose). With
the skill, both CSV runs added a "fails before, passes after" check, and one also
required multiline and embedded-quote test cases. These are borderline additions,
since a regression test arguably implies the check. This is a small, single-model,
same-operator authoring comparison of prompt fidelity, not a measurement of
downstream task success.

## Redundant instructions

`SKILL.md` is within the size guidance, but three themes are stated more than once:

- Unresolved choices: section 1 (ask one focused question, contradictory requirements)
  and section 3 (unresolved decisions kept separate, equally plausible targets,
  missing bug details, INFERRED and UNRESOLVED items).
- No-change logic: section 3 (decide before drafting) and section 5 (the no-change
  outcome and its sentence).
- Authorization: section 1 (preserve granted authority) and section 3 (no added
  grants, "be autonomous", release triggers, authorized epics).

Consolidating them might save about 300–400 tokens. Each repetition was added to fix
a fidelity failure observed in earlier evaluations (see the fidelity and quality
ledgers), and the current runs show no failure that removing them would address. The
text is kept until an A/B run shows that a consolidated version is at least as
faithful.

## Official standards source

`references/sources.json` adds provider `agentskills` (`agentskills.io`) with policy
`classification: standard`. Its sources are the specification, description
optimization, skill evaluation and the `llms.txt` index. They use the new role
`standard` (and `index`), and their applicability says they are a format and
authoring standard, not model-specific prompting guidance. The validator enforces the
separation: only standards providers may use the `standard` role, and a standard
cannot back a recommendation in `knowledge.json`. A local read-only freshness run
fetched all 31 sources (HTTP 200 or 304). The four new sources were added to
`sources-baseline.json`. Of the existing sources, only the `platform.claude.com/llms.txt`
index changed; no guidance page changed.

## Freshness schedule

Schedule 4486529 (daily, `17 6 * * *`) stays **inactive**. The namespace is on the Free
plan, and this account's CI usage for October is already far above the included
allowance, so remaining included minutes cannot be confirmed without new spending.
This follows `docs/freshness.md`; the job remains available manually.

## Observations not fixed here

- One with-skill answer (`ab-unresolved-with-1`) linked the local plugin-cache path
  of `SKILL.md` in its explanation outside the prompt. The path is redacted in the
  stored output. This is a minor disclosure of local context in author notes; record
  it for a future evaluation case before changing instructions.
- Explicit invocation still allows the no-change outcome (P1); that is intended.

## ChatGPT limits

Codex evidence does not show ChatGPT behavior. ChatGPT installation and activation
remain unobserved: this session had no authenticated ChatGPT access, and the
previously recorded app-policy refusal for Computer Use still applies. The reviewer
cases are written so the owner can repeat them in ChatGPT after installing from a
workspace upload or the directory.

Developed by the dondego.com team.
