# PromptingCraft.com

Website: [promptingcraft.com](https://promptingcraft.com)

The product is publicly named PromptingCraft.com. Since 0.3.0 the skill and plugin
identifier is `promptingcraft` (formerly `promptcraft`); see the
[migration notes](docs/migration-0.3.0.md).

Turn a development discussion into a prompt a fresh coding agent can execute.
PromptingCraft.com preserves the task contract, consults applicable official guidance,
drafts, critiques once, revises when necessary, and checks that requirements and permissions
survived. The assistant writing the prompt and the agent executing it may differ.
Targets: **Claude Code and OpenAI Codex**; **Cursor** is supported as a target agent
(see [Use in Cursor](#use-in-cursor)). Package metadata: **0.3.0**
(unreleased candidate; no 0.2.0 or 0.3.0 tag or release exists).

The immutable v0.1.0 tag is the canonical release. `main` contains unreleased
knowledge, contract-fidelity, local plugin integration and listing-metadata work. The latest
[contract-fidelity sample](evals/results/fidelity/README.md) found 0/14 material
drift after earlier diagnostic variance; it is not a guarantee. Native Codex
invocations are verified. ChatGPT-native activation and downstream superiority
remain unverified. Development CI archives do not replace v0.1.0 release assets.

When the original task is already suitable, PromptingCraft.com can return:
"The original prompt is already suitable. No material revision is necessary."
It preserves the original text; no-change still requires contract and source checks.

It helps produce a usable handoff; it cannot supply missing access, authority,
repository evidence or guarantees of downstream correctness.

**Canonical and only public source:** [GitLab](https://gitlab.com/revanalex/promptingcraft-skill).
A GitHub mirror exists but is not publicly reachable while an account visibility
issue is unresolved, so it is not offered as a public source.
Contribute through GitLab issues and merge requests. GitLab CI is authoritative;
GitHub Actions are not enabled.

## Two ways to use it

Use PromptingCraft as a standalone Agent Skill, or connect its MCP server for structured
access to official AI-developer guidance.

| | Standalone Agent Skill | Skill + MCP server |
| --- | --- | --- |
| What you install | `skills/promptingcraft/` (instructions and dated references) | The plugin: the same skill plus `mcp.json` |
| Hosts | Codex, Claude Code and Cursor (local skill folders) | Hosts that load the plugin's MCP server; verified in Codex |
| Prompt authoring (contract, draft, critique, final, no-change) | Yes | Yes, same skill |
| Official guidance | Bundled curated references, dated; the host's own documentation search or browsing when available | Also `search_guidance` and `get_guidance`: records with provenance and applicability |
| Freshness | Live only when the host actually reads an official page in that run; otherwise labeled dated cached | `check_source_freshness` compares one official page with its verified snapshot (cached up to 15 minutes) |
| Network | None required | HTTPS to `https://mcp.promptingcraft.com/mcp` (fixed categories and ids only; see [privacy](https://promptingcraft.com/privacy)) |
| If guidance retrieval fails | Uses bundled references and says so | Says the server was unavailable, then uses other official sources or bundled references |

The MCP server is optional. It supplies evidence, not authority: the skill still extracts
the contract, drafts, critiques and finalizes, and the user's requirements and permissions
always win. Neither mode guarantees real-time documentation: bundled references carry their
retrieval dates, and a freshness check shows only whether a page changed since it was
verified. Records of kind `promptingcraft_methodology` are PromptingCraft.com's own method,
not provider recommendations. Server details: [mcp/README.md](mcp/README.md) and
[data boundary](docs/mcp-data-boundary.md).

## A small example

Ask: "Write a Codex task: Save shows success after an API error. Preserve the
API shape; don't deploy."

Draft: "Fix saving and run tests."

Critique: the draft lost the symptom, API constraint and deployment boundary.

Final:

```text
Fix Save so an unsuccessful API response is not reported as success. Preserve
the API shape. Locate the existing save path and verify the requested failure
behavior. Do not deploy.

Optional suggestion: use the existing error-display pattern if one is available.
```

This is an original illustration, not proof of improved execution. See the
[worked examples](skills/promptingcraft/references/examples.md) and
[evaluation protocol](evals/README.md).

## Use in ChatGPT

The PromptingCraft.com plugin bundles the skill and declares one optional remote MCP server
(the guidance server, no account or credentials). Build its
local source once, register the real repository root, and install through supported
Codex or ChatGPT Desktop plugin controls. See the exact
[local installation and ChatGPT procedure](docs/chatgpt-installation.md).
After installation, start a new chat; explicitly select PromptingCraft.com with `@` or
ask **“Prepare a Codex prompt for this task.”** It uses the established discussion
and returns the final execution prompt in one copyable code block.

Current OpenAI documentation supports plugins in Chat, but local-source and
account availability vary. Codex CLI installation is verified separately from
ChatGPT Desktop and ordinary Chat activation. Computer Use cannot access ChatGPT
in this environment; those native checks remain a documented owner-side gate.
No repeated SKILL.md paste or upload is part of the supported installation route.
With unavailable retrieval, source guidance remains dated/unavailable.

## Install the standalone skill

Download the v0.1.0 skill archive and `SHA256SUMS` from
[GitLab v0.1.0](https://gitlab.com/revanalex/promptingcraft-skill/-/releases/v0.1.0).
Verify checksums before extracting. There is no 0.2.0 release yet; a clone
provides the current candidate:

```sh
git clone https://gitlab.com/revanalex/promptingcraft-skill.git
cd promptingcraft-skill
python3 scripts/install_skill.py --host codex --project-dir /path/to/your/project
# Or, for Claude Code:
python3 scripts/install_skill.py --host claude --project-dir /path/to/your/project
# Or, for Cursor:
python3 scripts/install_skill.py --host cursor --project-dir /path/to/your/project
```

The optional installer requires Python 3.11+, refuses existing targets and touches
only the explicitly chosen project's skill directory. You can instead copy the
extracted `promptingcraft/` directory yourself into `.agents/skills/` (Codex) or
`.claude/skills/` (Claude Code) or `.cursor/skills/` (Cursor; Cursor also reads
`.agents/skills/`), including all its references and license.
Restart the host if discovery has not refreshed. In Codex invoke `$promptingcraft`;
in Claude Code invoke `/promptingcraft`, then describe the prompt you need.
No development task is executed by the skill.

## Use in Cursor

Cursor reads Agent Skills from `.cursor/skills/` or `.agents/skills/` in a project and
from `~/.cursor/skills/` for the user. The plugin root (`plugin.json` with the Agent
Plugins 1.0.0 schema and `skills/promptingcraft/`) follows Cursor's documented Agent Plugins
format; it has not been submitted to or reviewed by the Cursor Marketplace.

When the executor is Cursor, PromptingCraft.com loads its
[Cursor notes](skills/promptingcraft/references/cursor.md): under Auto the underlying model
is treated as unknown, so no Claude, GPT or Composer prompting rules are applied unless
the selected model is established.

Measured in the Cursor CLI ([cursor activation eval](evals/results/cursor-trigger-1/README.md)):
with the default Auto setting (reported as Composer 2.5 Fast) the skill was available
but did not activate automatically (0/30 prompt requests); naming it, as in
**“Use the promptcraft skill to prepare a Cursor prompt for this task”** (the 0.2.0
identifier), loaded it 2/2. With 0.3.0, name it `promptingcraft`.
In the editor you can also pick it from the `/` menu. Activation depends on the selected
model. Plugin loading in the Cursor editor has not been tested.

## Plugin package

The plugin ZIP includes root `plugin.json` using Agent Plugins 1.0.0, one
`skills/promptingcraft/` tree, listing icons/logos under `assets/` and a Claude
Code compatibility manifest, plus a root `mcp.json` that declares the optional guidance
MCP server. It declares no hooks or credentials.
Its ChatGPT listing metadata (display name, descriptions, website, support,
privacy and terms URLs, brand colors and icons) is checked by the validator;
it has not been submitted to or reviewed by any plugin directory. In Claude
Code, session-only loading is:

```sh
claude --plugin-dir /path/to/extracted/promptingcraft-plugin
# In that session: /promptingcraft:promptingcraft
```

The repository already includes `.agents/plugins/marketplace.json` for
`dondego-local`. Prepare its actual plugin directory before registration:

```sh
python3 scripts/prepare_marketplace.py
python3 scripts/validate.py --marketplace
```

The generated `dist/promptingcraft-plugin/` comes from the canonical skill using the
existing reproducible archive builder. It is a snapshot, not a second maintained
skill. The catalog resolves its path relative to the repository root. See
[installation, refresh and removal](docs/chatgpt-installation.md).

## Verification and freshness

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
python3 scripts/package.py --output dist
python3 scripts/prepare_marketplace.py
python3 scripts/validate.py --marketplace
# Optional live maintenance, kept separate from merge checks:
python3 scripts/freshness.py --output /tmp/promptingcraft-freshness --write-baseline
```

Normal checks are deterministic, offline and use synthetic documents. Live source
checks compare usable normalized content hashes, use HTTP validators when supplied
and discover candidate links in official indexes. They report changed, unchanged,
new, missing/unavailable and partial/error states. They neither prove guidance is
correct nor automatically change the skill. Fetch time is not publication time.
Caches and raw model traces stay outside tracked content; reports contain metadata,
not wholesale provider documentation.

See [freshness operation and schedule gate](docs/freshness.md),
[verified source decisions](docs/sources.md), [actual verification](docs/verification.md)
and the [bounded roadmap](docs/roadmap.md). Source guidance is revalidated during
skill use when host network capabilities permit; offline notes are never current.

## Scope and license

MIT licensed original content. No official OpenAI/Anthropic affiliation or
endorsement. No hosted app, telemetry, sign-up, model router, API billing,
marketplace submission, deployment or automatic instruction rewriting in v0.1
or the 0.2.0 candidate.
See [LICENSE](LICENSE), [CONTRIBUTING](CONTRIBUTING.md), [SECURITY](SECURITY.md)
and [CHANGELOG](CHANGELOG.md).

Developed by the [dondego.com](https://dondego.com) team.
