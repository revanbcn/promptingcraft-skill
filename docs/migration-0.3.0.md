# Migrating from `promptcraft` to `promptingcraft` (0.3.0)

From 0.3.0 the skill and plugin identifier is `promptingcraft`, matching the public name
PromptingCraft.com. Versions up to 0.2.0 (including the v0.1.0 release) used `promptcraft`.
There is one skill; the old identifier is not maintained in parallel. Existing
installations keep working until you replace them, but receive no updates.

| | Before (≤ 0.2.0) | From 0.3.0 |
| --- | --- | --- |
| Skill folder | `skills/promptcraft/` | `skills/promptingcraft/` |
| Codex | `$promptcraft` | `$promptingcraft` |
| Claude Code (standalone skill) | `/promptcraft` | `/promptingcraft` |
| Claude Code (plugin) | `/promptcraft:promptcraft` | `/promptingcraft:promptingcraft` |
| Codex local marketplace plugin | `promptcraft@dondego-local` | `promptingcraft@dondego-local` |
| Plugin archive | `promptcraft-plugin-<version>.zip` | `promptingcraft-plugin-<version>.zip` |

## Codex plugin from the local marketplace

```sh
git pull                                   # in your clone of promptingcraft-skill
python3 scripts/prepare_marketplace.py     # regenerates dist/promptingcraft-plugin
codex plugin add promptingcraft@dondego-local
# check that $promptingcraft works in a new session, then remove the old plugin:
codex plugin remove promptcraft@dondego-local
```

## Standalone skill folders

Install the new folder first (`python3 scripts/install_skill.py --host codex|claude|cursor
--project-dir <project>`), confirm the host lists `promptingcraft`, then delete the old
`promptcraft` folder from the same place (`.agents/skills/`, `.claude/skills/` or
`.cursor/skills/`, in the project or in your home directory). Keeping both makes
the host list two copies of the same skill.

## What did not change

The repository URLs, the MCP endpoint `https://mcp.promptingcraft.com/mcp`, its tool names
and the prompt-authoring behavior. In the MCP tools, the record kind
`promptcraft_methodology` is now `promptingcraft_methodology`, and the ledger fields
`promptcraft_applicability` and `promptcraft_adaptations` are now `promptingcraft_*`
(ledger `schema_version` 2).
Historical evaluation evidence under `evals/results/` keeps the identifier it was
recorded with.

Developed by the dondego.com team.
