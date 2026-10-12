# Changelog

## Unreleased — EPIC 8: public launch and marketplace readiness

- Cursor as a target agent: `references/cursor.md` (Auto treated as an unknown model),
  cursor.com docs classified `agent-product` (cannot back model prompting advice),
  `install_skill.py --host cursor`, and native Cursor CLI activation results
  (`evals/results/cursor-trigger-1/`: automatic 0/30 with Auto, named 2/2).
- Listing metadata: `capabilities` (6), `keywords` (11), new starter prompts, long
  description naming Cursor, the published evaluation and the absence of a prompt backend.
- `.cursor-plugin/marketplace.json` for the single root plugin; `docs/cursor-submission.md`.
- Published A/B evidence: grader verdicts and prompt, run log and runner
  (`scripts/evaluate_ab.py`); trigger eval host failures corrected to 5 of 65 attempts.
- Worked examples: each lists its contract; new Cursor investigation, prompt review,
  no-change and official-guidance examples (authored illustrations, not eval results).
- Package stays 0.2.0 (unreleased); no tag or release created.

## Unreleased — Agent Skills standard audit

- `skills-ref validate` passes for the source skill and both ZIPs; specification,
  progressive disclosure and resource references comply (`docs/agent-skills-audit.md`).
- Activation eval per agentskills.io: 20 queries, fixed train/validation split, 3 runs
  each, counted only from actual `SKILL.md` loads (`scripts/evaluate_triggers.py`,
  `evals/trigger/queries.json`, `evals/results/trigger-1/`). Description unchanged.
- Native reviewer-case outputs and a blinded with/without comparison
  (`evals/results/review-native/`, `evals/results/ab-1/`).
- agentskills.io added as a separately classified official standards source
  (`classification: standard`, role `standard`), never prompting guidance.
- No `SKILL.md` instruction change; daily freshness schedule stays inactive.

## Unreleased — 0.2.0 candidate: OpenAI Plugins Directory readiness

- Listing metadata for a Skills-only submission: category Developer Tools, short
  description "Source-backed agent prompts", a clearer long description with explicit
  limits and independence, and three starter prompts (no @mentions).
- The validator enforces directory rules offline: category list, at most three unique
  one-line starter prompts of 128 characters, no screenshots, and no apps, hooks or MCP
  settings; `package.py` checks the plugin ZIP against the skills-only archive rules.
- Reviewer-reproducible cases in `evals/review/cases.json` (6 positive, 4 negative; P7, a
  Cursor agent task, was added later for the directory submission) and the
  field-by-field submission guide `docs/openai-submission.md`.
- No skill instruction change, no onboarding skill, no MCP server, no release or submission.

## Unreleased — 0.2.0 candidate: PromptingCraft.com brand and plugin readiness

- Public brand is PromptingCraft.com (https://promptingcraft.com). The skill and
  plugin identifier stays `promptcraft` for compatibility with existing
  installations, so invocations, archive names and the generated
  `dist/promptcraft-plugin` are unchanged.
- ChatGPT listing metadata: display name, 30-character short description, honest
  long description, website, support, privacy and terms URLs, brand colors, and
  light/dark icons and logos packaged under `assets/`. The validator checks text
  limits, https URLs, package-relative square SVG/PNG assets, brand-color contrast
  and skill/manifest display consistency.
- Canonical repository URL becomes https://gitlab.com/revanalex/promptingcraft-skill.
- Minor version: new metadata and packaged assets, no identifier or behavior
  change. No directory submission, MCP server, tag or release.

## Unreleased — contract fidelity and native validation

- Preserve expressly immutable text verbatim; do not infer whole-file freezes.
- Preserve discussion/implementation mode, unresolved choices and planning freedom.
- Reject invented API exceptions and blanket overrides of host/project authority.
- Allow no-change when the original task is suitable; keep necessary corrections.
- Optional checker adds exact-literal, local action and no-change identity checks.
- Frozen A/B/C source experiment, stricter artifact acceptance, observed tool/source
  metrics and honest timeout collection; no effectiveness claim from source quality.
- Native packaged Codex evidence and evaluation results are recorded separately.
- Canonical v0.1.0 release, tag and public assets remain unchanged.

## Unreleased — official knowledge and contract quality

- Curated, attributed official recommendations with applicability and limits.
- Five requirement classes and bidirectional final-clause provenance review.
- Optional offline annotation-assisted contract checker; semantic review required.
- All-case baseline/candidate evaluation, four realistic public scenarios and a
  bounded isolated downstream protocol; results reported separately.
- Preserve portable packaging while omitting Python bytecode caches.
- No new release/tag/version or hosted API dependency.

## 0.1.0 — 2026-10-12

- One portable prompt-authoring skill for Claude Code and Codex handoffs.
- Contract extraction, applicable guidance, bounded critique and drift check.
- Original provider summaries, sources, rubric and worked examples.
- Read-only source freshness comparison and index candidate discovery.
- Deterministic fixture checks, isolated installation and reproducible archives.
- Synthetic behavior evaluation protocol, with results reported separately.
- GitLab canonical CI/review route; explicit GitHub mirror, no Actions.

Developed by the [dondego.com](https://dondego.com) team.
