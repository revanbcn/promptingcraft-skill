# PromptCraft by DondeGo

Turn a development discussion into a prompt a fresh coding agent can execute.
PromptCraft preserves the task contract, consults applicable official guidance,
drafts, critiques once, revises when necessary, and checks that requirements and permissions
survived. The assistant writing the prompt and the agent executing it may differ.
First targets: **Claude Code and OpenAI Codex**. Version: **0.1.0**.

The immutable v0.1.0 tag is the canonical release. `main` contains unreleased
knowledge, contract-fidelity and local plugin integration work. The latest
[contract-fidelity sample](evals/results/fidelity/README.md) found 0/14 material
drift after earlier diagnostic variance; it is not a guarantee. Native Codex
invocations are verified. ChatGPT-native activation and downstream superiority
remain unverified. Development CI archives do not replace v0.1.0 release assets.

When the original task is already suitable, PromptCraft can return:
"The original prompt is already suitable. No material revision is necessary."
It preserves the original text; no-change still requires contract and source checks.

It helps produce a usable handoff; it cannot supply missing access, authority,
repository evidence or guarantees of downstream correctness.

**Canonical:** [GitLab](https://gitlab.com/revanalex/promptcraft-skill).
**Mirror:** [GitHub](https://github.com/revanbcn/promptcraft-skill) (configured public;
unauthenticated readback returned 404 at release preparation, so public access is
not verified).
Contribute through GitLab issues and merge requests. GitLab CI is authoritative;
GitHub Actions are not enabled. Mirroring is an explicit verified dual push of
`main` and release tags; ongoing automatic mirroring is not configured.

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
[worked examples](skills/promptcraft/references/examples.md) and
[evaluation protocol](evals/README.md).

## Use in ChatGPT

PromptCraft is a skills-only plugin with no MCP server or credentials. Build its
local source once, register the real repository root, and install through supported
Codex or ChatGPT Desktop plugin controls. See the exact
[local installation and ChatGPT procedure](docs/chatgpt-installation.md).
After installation, start a new chat; explicitly select PromptCraft with `@` or
ask **“Prepare a Codex prompt for this task.”** It uses the established discussion
and returns the final execution prompt in one copyable code block.

Current OpenAI documentation supports plugins in Chat, but local-source and
account availability vary. Codex CLI installation is verified separately from
ChatGPT Desktop and ordinary Chat activation. Computer Use cannot access ChatGPT
in this environment; those native checks remain a documented owner-side gate.
No repeated SKILL.md paste or upload is part of the supported installation route.
With unavailable retrieval, source guidance remains dated/unavailable.

## Install the standalone skill

Download the skill archive and `SHA256SUMS` from
[GitLab v0.1.0](https://gitlab.com/revanalex/promptcraft-skill/-/releases/v0.1.0)
or the [GitHub release](https://github.com/revanbcn/promptcraft-skill/releases/tag/v0.1.0).
Verify checksums before extracting. A clone works too:

```sh
git clone https://gitlab.com/revanalex/promptcraft-skill.git
cd promptcraft-skill
python3 scripts/install_skill.py --host codex --project-dir /path/to/your/project
# Or, for Claude Code:
python3 scripts/install_skill.py --host claude --project-dir /path/to/your/project
```

The optional installer requires Python 3.11+, refuses existing targets and touches
only the explicitly chosen project's skill directory. You can instead copy the
extracted `promptcraft/` directory yourself into `.agents/skills/` (Codex) or
`.claude/skills/` (Claude Code), including all its references and license.
Restart the host if discovery has not refreshed. In Codex invoke `$promptcraft`;
in Claude Code invoke `/promptcraft`, then describe the prompt you need.
No development task is executed by the skill.

## Plugin package

The plugin ZIP includes root `plugin.json` using Agent Plugins 1.0.0, one
`skills/promptcraft/` tree and a Claude Code compatibility manifest. It declares
no MCP servers, hooks or credentials. In Claude Code, session-only loading is:

```sh
claude --plugin-dir /path/to/extracted/promptcraft-plugin
# In that session: /promptcraft:promptcraft
```

The repository already includes `.agents/plugins/marketplace.json` for
`dondego-local`. Prepare its actual plugin directory before registration:

```sh
python3 scripts/prepare_marketplace.py
python3 scripts/validate.py --marketplace
```

The generated `dist/promptcraft-plugin/` comes from the canonical skill using the
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
python3 scripts/freshness.py --output /tmp/promptcraft-freshness --write-baseline
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
marketplace submission, deployment or automatic instruction rewriting in v0.1.
See [LICENSE](LICENSE), [CONTRIBUTING](CONTRIBUTING.md), [SECURITY](SECURITY.md)
and [CHANGELOG](CHANGELOG.md).

Developed by the [dondego.com](https://dondego.com) team.
