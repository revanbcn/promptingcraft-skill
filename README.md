# PromptCraft by DondeGo

Turn a development discussion into a prompt a fresh coding agent can execute.
PromptCraft preserves the task contract, consults applicable official guidance,
drafts, critiques once, revises, and checks that requirements and permissions
survived. The assistant writing the prompt and the agent executing it may differ.
First targets: **Claude Code and OpenAI Codex**. Version: **0.1.0**.

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
Fix the settings Save button so an unsuccessful API response shows an error
instead of success. Preserve the existing API shape and follow nearby UI patterns.
Locate the save handler and its callers, reproduce the failure and make the
smallest root-cause fix. Verify successful saving and API-error behavior,
including that the error path never shows success; run the affected checks.
Do not deploy. Report changed files, commands/results and remaining gaps.
```

This is an original illustration, not proof of improved execution. See the
[worked examples](skills/promptcraft/references/examples.md) and
[evaluation protocol](evals/README.md).

## Use in ordinary ChatGPT chat

No terminal, Python, Git credentials, paid API key or new MCP is needed to compose.
Open [SKILL.md](skills/promptcraft/SKILL.md), paste its contents into the chat and
ask it to apply PromptCraft to your discussion. Provide the relevant supporting
files as text or attachments when requested; all are in the standalone package.
If browsing is available, use it to retrieve the applicable official pages.
Without browsing, the assistant should explicitly label its source guidance dated
or unavailable and avoid claiming current model-specific tuning.

This manual use is prompt context, **not native skill installation**. A public Git
repository is not a listed ChatGPT directory plugin. Native plugin packaging is
prepared; directory submission and account-specific installation are separate,
excluded gates. Ordinary-ChatGPT runtime verification has not been established
by a terminal test. See [surface status](docs/verification.md).

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

For ChatGPT/Codex desktop local plugin setup, follow the currently documented
[repo marketplace procedure](https://developers.openai.com/plugins/build/plugins#install-a-local-plugin-manually):
copy the extracted plugin into `plugins/promptcraft` in a chosen project and create
that project's `.agents/plugins/marketplace.json` entry pointing to
`./plugins/promptcraft`. Installation requires the supported desktop plugin UI;
this repository does not configure a user's global plugin source automatically.
The standalone Codex installation above is the simpler v0.1 route.

## Verification and freshness

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
python3 scripts/package.py --output dist
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
