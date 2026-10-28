# PromptingCraft.com — plugin package 0.4.0

Website: https://promptingcraft.com

Turn a development discussion into an execution-ready prompt for Claude Code or
Codex: preserve the contract → consult applicable guidance → draft → critique →
finalize → check requirements and authority boundaries. This package composes
prompts; it does not execute the underlying development task.

One portable skill at `skills/promptingcraft/SKILL.md` and its bundled references,
listing icons/logos under `assets/`, MIT license, root Agent Plugins 1.0.0 manifest
and Claude Code adapter are included. Since 0.3.0 the skill and plugin identifier is
`promptingcraft` (formerly `promptcraft`; see [migration notes](https://gitlab.com/revanalex/promptingcraft-skill/-/blob/main/docs/migration-0.3.0.md)).
The root `mcp.json` declares one remote MCP server, the PromptingCraft.com guidance
server at `https://mcp.promptingcraft.com/mcp`; the skill also works without it. There
are no credentials or hooks. This archive is a separate upgrade candidate; the existing published ChatGPT plugin remains version 0.3.0 until an explicitly approved update is accepted.

For session-only Claude Code loading, run:

```sh
claude --plugin-dir /path/to/promptingcraft-plugin
# Then invoke /promptingcraft:promptingcraft
```

For a standalone Codex installation, copy the complete `skills/promptingcraft`
directory into the chosen project's `.agents/skills/`; restart if needed and
invoke `$promptingcraft`. For Claude Code standalone use `.claude/skills/` and
`/promptingcraft`. Refuse accidental replacement of an existing skill.

For native local Codex/ChatGPT Desktop installation, use the repository's
[one-time marketplace setup](https://gitlab.com/revanalex/promptingcraft-skill/-/blob/main/docs/chatgpt-installation.md).
It includes a real catalog and reproducibly generated plugin source; no repeated
pasting of SKILL.md is required. After installation, start a new chat and select
PromptingCraft.com with `@` in ChatGPT or `$promptingcraft` in Codex, or ask to prepare a
Codex prompt. Local source/account availability varies. Codex installation does
not establish ChatGPT installation or ordinary Chat activation. Without usable
retrieval, guidance remains dated/unavailable, never current. Actual ChatGPT UI
validation is a separate operator gate.

Maintenance scripts, tests, evaluations and full installation/distribution docs
are in the [canonical GitLab repository](https://gitlab.com/revanalex/promptingcraft-skill),
and [public GitHub mirror](https://github.com/revanbcn/promptingcraft-skill). GitLab remains the contribution and CI authority.
See the repository's verification receipt for actual runtime and CI status.

Developed by the [dondego.com](https://dondego.com) team.
