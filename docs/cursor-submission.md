# Cursor Marketplace submission — PromptingCraft.com

Prepared 2026-10-12 against the official pages listed under **Sources**. Nothing here has
been submitted, no publisher application has been made and no terms have been accepted.

## Status

| Item | State |
| --- | --- |
| Plugin format | Prepared: the repository root is an Agent Plugins 1.0.0 plugin (`plugin.json` with `$schema`, `skills/promptcraft/SKILL.md`), the format Cursor documents for Agent Plugins |
| Catalog | Prepared: `.cursor-plugin/marketplace.json` lists the single root plugin (`source: "./"`) with category, tags and an absolute logo URL |
| Public repository | Verified: https://gitlab.com/revanalex/promptingcraft-skill is public and MIT licensed |
| GitLab accepted for public listing | **Unverified**: the docs say "public Git repository"; relative logos resolve to raw.githubusercontent.com and source refresh mentions the Cursor GitHub App. GitHub visibility is unresolved, so the GitLab URL is the one to submit |
| Native activation in Cursor | Measured in the Cursor CLI, see **Native checks**; editor plugin loading **not tested** |
| Publisher application, terms, submission | **Owner only**; not done (cursor.com/marketplace/publish requires sign-in) |
| Form fields of the publish page | **Unverified**: not visible without signing in |

## Checklist from the Cursor plugin reference

| Item | State | Evidence |
| --- | --- | --- |
| Valid manifest | Prepared | `plugin.json` validates against the Agent Plugins 1.0.0 JSON Schema; `scripts/validate.py` |
| Unique lowercase kebab-case name | Prepared | `promptcraft` (stable id kept for existing installations; display name PromptingCraft.com) |
| Clear description | Prepared | Manifest `description` and catalog entry `description` |
| Valid component files and frontmatter | Prepared | One skill; `name: promptcraft` matches its folder; `description` present; `skills-ref validate` passes |
| Logo | Prepared | Absolute `https://gitlab.com/revanalex/promptingcraft-skill/-/raw/main/assets/logo.svg` (a relative path would resolve to GitHub) |
| README documenting usage | Prepared | `README.md`, section "Use in Cursor" |
| No undeclared variables or credentials | Verified | No `mcp.json`, `variables`, hooks, rules, agents or commands (`tests/test_marketplace.py`) |
| Manifest paths relative, no `..` | Verified | Catalog `source` is `./`; no component paths declared |
| Tested locally | Partly | Cursor CLI native checks below; editor reload not exercised |
| One maintained implementation | Verified | No Cursor-specific copy of the skill; no `.cursor-plugin/plugin.json` |

## Listing text (copy-ready)

| Field | Value |
| --- | --- |
| Display name | PromptingCraft.com |
| Plugin id | `promptcraft` |
| Repository | https://gitlab.com/revanalex/promptingcraft-skill |
| Description | An open-source skill that turns development discussions into reviewed, execution-ready coding-agent prompts using official AI-developer guidance. Developed by the dondego.com team. |
| Category (catalog) | Developer Tools |
| Tags (catalog) | Agent Skills, Prompt Engineering, Coding Agents, Codex, Claude Code, Cursor, Developer Tools |
| Website | https://promptingcraft.com |
| Support | https://promptingcraft.com/contact |
| Privacy / Terms | https://promptingcraft.com/privacy, https://promptingcraft.com/terms |
| License | MIT |

Usage examples for reviewers:

1. "Use the promptcraft skill to turn this discussion into a Cursor Agent prompt; investigation only."
2. "Use the promptcraft skill to review this handoff without changing its scope." (paste a prompt)
3. "Use the promptcraft skill: is this Codex task already suitable? Keep it unchanged if so."

## Cursor-specific behavior

`references/cursor.md` is loaded for a Cursor executor. Under Auto, Cursor selects the model
per request, so the executor model is treated as unknown and only agent/general guidance is
applied; Claude, GPT, Gemini or Composer prompting rules are applied only when the selected
model is established. Plan and Ask modes are reflected as scope in the task text, never as
granted authority. Cursor documentation is classified `agent-product` in
`references/sources.json`: it is official for Cursor behavior and cannot back a model
prompting recommendation (enforced by `scripts/validate.py`).

## Native checks

`evals/results/cursor-trigger-1/` (Cursor CLI 2026.10.01-e373342, default Auto, reported as
Composer 2.5 Fast):

- Automatic activation: 0/30 positive runs and 0/30 negative runs; the skill was listed as
  available. Automatic activation is therefore not established in Cursor.
- Explicit naming ("Use the promptcraft skill …"): 2/2 loaded.
- Diagnostic with `gpt-5.3-codex`: 3/5 positive queries loaded once each.
- Behavior spot check (ungraded): scope and open decisions preserved; extra mandatory steps
  added, which the project counts as fidelity defects.
- Plugin loading through `--plugin-dir` or `~/.cursor/plugins/local/` was not observed in the
  CLI; the Cursor editor was not tested.

## Remaining owner steps

1. Sign in at https://cursor.com/marketplace/publish and read the publisher application and
   terms; decide whether to apply.
2. Confirm whether a GitLab repository is accepted for public listing; if only GitHub is
   accepted, resolve the GitHub mirror visibility first.
3. Optionally install the plugin in the Cursor editor (Customize → plugins, or
   `~/.cursor/plugins/local/promptcraft` and "Developer: Reload Window") and confirm the
   skill appears and loads when named.
4. Submit the repository URL only after the website and skill merge requests are merged.

## Sources

- https://cursor.com/docs/plugins
- https://cursor.com/docs/reference/plugins
- https://cursor.com/docs/skills
- https://cursor.com/marketplace/publish (sign-in required)
- https://cursor.com/docs/agent/prompting, https://cursor.com/docs/agent/plan-mode,
  https://cursor.com/docs/models-and-pricing
- https://agent-plugins.org/schemas/1.0.0/plugin.schema.json

Developed by the dondego.com team.
