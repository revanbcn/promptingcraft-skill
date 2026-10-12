# Changelog

## Unreleased — 0.2.0 candidate: OpenAI Plugins Directory readiness

- Listing metadata for a Skills-only submission: category Developer Tools, short
  description "Source-backed agent prompts", a clearer long description with explicit
  limits and independence, and three starter prompts (no @mentions).
- The validator enforces directory rules offline: category list, at most three unique
  one-line starter prompts of 128 characters, no screenshots, and no apps, hooks or MCP
  settings; `package.py` checks the plugin ZIP against the skills-only archive rules.
- Reviewer-reproducible cases in `evals/review/cases.json` (6 positive, 4 negative) and the
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
