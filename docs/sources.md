# Official source and packaging decisions

For the new curated selection, see [knowledge acquisition](knowledge-acquisition.md)
and the [portable recommendation ledger](../skills/promptingcraft/references/knowledge.json).
The quality-1 live check retrieved all 27 registry sources successfully; its
accepted metadata baseline is separate from semantic recommendation review.
The original v0.1.0 source decisions below remain historical.

Retrieved on **2026-10-12 Europe/Madrid** (live maintenance snapshot began
**2026-10-11T22:41:08Z**). These are retrieval observations, not publication dates.
Source publication/update times were not established. Original project summaries
are distributed; provider documents and private traces are not.

## 2026-10-28 targeted source additions

The official [DeepSeek thinking-mode guide](https://api-docs.deepseek.com/guides/thinking_mode/)
and [Kimi thinking-model guide](https://platform.kimi.ai/docs/guide/use-thinking-models)
were read and their normalized content captured on 2026-10-28T17:22:56Z. The new
records cover provider-specific API reasoning context and tool calls, including
Kimi K3.1 Pro and K2.7 Code. They are not generic prompting directives and do not
establish support for all models or coding clients. Exact source hashes and resolved
URLs are in the baseline; no publication or update date is inferred. Existing
2026-10-12 recommendations remain dated, pending separate revalidation. The deployed
MCP and published OpenAI plugin are unchanged until separately released.

## Authoring and behavior

| Canonical URL actually checked | Scope / decision |
| --- | --- |
| https://agentskills.io/specification | YAML name/description, portable resources, progressive disclosure |
| https://agentskills.io/skill-creation/best-practices | One coherent job, calibrated detail, learn from actual runs |
| https://agentskills.io/skill-creation/evaluating-skills | Start with 2–3 clean paired cases; distinguish assertions from judgment |
| https://github.com/anthropics/skills | Official repository inspected for ecosystem/license context; no copied skills |
| https://github.com/openai/skills | Official repository inspected; no copied skills or private history |
| https://learn.chatgpt.com/docs/prompting | Codex section: behavior, context, constraints and verification |
| https://learn.chatgpt.com/docs/build-skills | Focused triggers, instruction-first workflow, local skill discovery |
| https://developers.openai.com/plugins/build/skills | Progressive disclosure and explicit user-priority guidance |
| https://developers.openai.com/api/docs/guides/latest-model#gpt-6-astra-instruction-following | GPT-6 Astra applicability only; no assumption that a target uses Astra |
| https://developers.openai.com/api/docs/guides/prompt-engineering | API prompt/message scope; not universal CLI task syntax |
| https://developers.openai.com/blog/eval-skills | Behavioral evals; metadata checks alone do not show improvement |
| https://code.claude.com/docs/en/best-practices | Context, verifiable outcomes, proportional exploration/planning |
| https://code.claude.com/docs/en/prompt-library | Outcome/reference/verification patterns; no wholesale copied prompts |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | Prompting is one intervention; define success and evidence first |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Living API/model routing; exact model scope required |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5 | Discovered and fetched through the living model reference; never transferred universally |

The OpenAI MCP search indexed `https://learn.chatgpt.com/guides/best-practices`,
but fetching its Markdown returned 404 in preflight. It is not treated as a
verified living guide; the successfully fetched prompting/build-skills pages
supply the applicable guidance. This failure is not proof the guidance was withdrawn.

## Packaging and distribution

| Canonical URL actually checked | Decision |
| --- | --- |
| https://developers.openai.com/plugins/build/plugins | Root portable manifest; `.codex-plugin` is a supported older fallback, not needed here |
| https://agent-plugins.org/specification | Agent Plugins directory and discovery contract |
| https://agent-plugins.org/schemas/1.0.0/plugin.schema.json | Actual JSON schema fetched; minimal manifest validated against it separately |
| https://code.claude.com/docs/en/plugins/manifest-reference | Claude Code `.claude-plugin/plugin.json` adapter; root skill tree |
| https://code.claude.com/docs/en/plugins/create | Session-only `--plugin-dir` and plugin skill namespace |
| https://developers.openai.com/learn/docs-mcp | Official docs MCP is optional host capability, not a bundled dependency |
| https://docs.gitlab.com/user/project/repository/mirror/push/ | Secure push mirror needs its own configuration; default here is verified dual push |
| https://docs.gitlab.com/ci/pipelines/schedules/ | Schedule ownership, runner/quota and activation gates |

The OpenAI plugin-creator guide currently describes a compatibility scaffold;
its output must not be blindly renamed to the portable format. No plugin-creator
tool was available in this session. The installed skill-creator initializer was
used, placeholders replaced, and its validator run. The portable manifest was
manually authored to the fetched schema. The Claude Code CLI strict validator
checks its own adapter; it does not certify a ChatGPT installation.

One skill tree, no empty MCP/hook scaffolding, no divergent host skills, no paid
model API dependency. Public Git distribution and local host loading do not mean
public-directory publication. Ordinary chat can use manual instruction context
without any plugin installation.

## Living discovery

The [machine-readable registry](../skills/promptingcraft/references/sources.json)
includes these actually fetched indexes:

- https://code.claude.com/docs/llms.txt
- https://platform.claude.com/llms.txt
- https://developers.openai.com/llms.txt
- https://developers.openai.com/api/llms.txt
- https://developers.openai.com/codex/llms.txt
- https://developers.openai.com/plugins/llms.txt

Search/read tools actually used from both docs MCP servers:
`search_claude_code_docs`, `query_docs_filesystem_claude_code_docs`,
`search_openai_docs`, `fetch_openai_doc`. Official pages were also read via web
retrieval. GitLab CI guidance was resolved and queried through Context7
(`/websites/gitlab`); local CLI flags were checked using installed help.
