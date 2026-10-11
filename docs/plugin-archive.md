# PromptCraft by DondeGo — plugin package 0.1.0

Turn a development discussion into an execution-ready prompt for Claude Code or
Codex: preserve the contract → consult applicable guidance → draft → critique →
finalize → check requirements and authority boundaries. This package composes
prompts; it does not execute the underlying development task.

One portable skill at `skills/promptcraft/SKILL.md` and its bundled references,
MIT license, root Agent Plugins 1.0.0 manifest and Claude Code adapter are included.
There are no MCP servers, credentials or hooks. A public Git release is not a
published ChatGPT directory plugin.

For session-only Claude Code loading, run:

```sh
claude --plugin-dir /path/to/promptcraft-plugin
# Then invoke /promptcraft:promptcraft
```

For a standalone Codex installation, copy the complete `skills/promptcraft`
directory into the chosen project's `.agents/skills/`; restart if needed and
invoke `$promptcraft`. For Claude Code standalone use `.claude/skills/` and
`/promptcraft`. Refuse accidental replacement of an existing skill.

Ordinary ChatGPT chat can receive SKILL.md as pasted instruction context plus
relevant supporting files; no local runtime or new MCP is needed for composition.
Without browsing, guidance is dated/unavailable, never current. Native desktop
plugin installation requires the supported UI and is a separate unverified gate.

Maintenance scripts, tests, evaluations and full installation/distribution docs
are in the [canonical GitLab repository](https://gitlab.com/revanalex/promptcraft-skill),
with a [GitHub mirror](https://github.com/revanbcn/promptcraft-skill). GitLab is the
contribution and CI authority. No automatic mirroring or monitoring is implied.
See the repository's verification receipt for actual runtime and CI status.

Developed by the [dondego.com](https://dondego.com) team.
