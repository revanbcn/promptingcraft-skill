# Claude Code routing notes

Load only for a Claude Code executor. Original summary checked 2026-10-12;
revalidate applicable pages during use. Offline notes remain dated cached guidance.

- Describe the outcome, give useful context, constraints and existing patterns,
  and include a test, build or visual check the executor can actually run.
- Exploration and planning help when the approach is uncertain; a small, clear
  fix can proceed directly. Show verification evidence in the completion receipt.
- Keep broadly applicable project instructions concise. Do not assume the
  executor has loaded CLAUDE.md or this conversation without evidence.
- Claude Code task guidance and Claude API prompt-building guidance have different
  scopes. API thinking/effort settings and tool protocol rules are not automatically
  controls available in a coding-agent user prompt.
- Anthropic's living prompting page now routes to separate model guides. Match
  the evidenced model exactly; do not assume a Claude Code session uses the latest
  model or apply another model's prompting rules universally.

Relevant curated records: `claude-clear`, `claude-progressive`,
`claude-code-authoring`, `claude-sonnet-scope`, `claude-json-reasoning`,
`claude-long-context`. Sonnet 5.5's scope/JSON guidance is specific to that model
and observed failure; do not transplant it to unknown executors. Long-document
ordering is conditional on large inputs. It does not require XML or quotations
for every small task. Helpful unrequested work remains optional.

Start with https://code.claude.com/docs/en/best-practices and
https://code.claude.com/docs/en/prompt-library. Use
https://code.claude.com/docs/llms.txt for agent discovery and
https://platform.claude.com/llms.txt for API/model guidance discovery. A discovered
link is only a candidate until its actual contents and applicability are checked.
