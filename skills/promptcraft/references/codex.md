# Codex routing notes

Load only for a Codex executor. Original summary checked 2026-10-12; revalidate
relevant sources during use. These dated notes are not a live freshness claim.

- Use the desired behavior, relevant code or reproduction steps, important
  constraints and an explicit way to verify the change. Include context that a
  fresh executor actually receives; do not assume this chat's files are shared.
- Plan first when scope warrants investigation. Avoid turning a small fix into
  a large planning ceremony. Require observable evidence, not a success assertion.
- Skills are progressively disclosed by description, then SKILL.md, then relevant
  resources. A concise, specific trigger and one recognizable job matter.
- Current OpenAI skill guidance links to GPT-6 Astra instruction-following notes.
  For that model, make the priority of explicit user instructions over skill
  guidelines clear. This does not establish Astra as the executor's model.
- API message hierarchy, reasoning effort, tool schemas and system-prompt design
  belong to API builders. Don't put API-only configuration into a user handoff
  for an existing Codex CLI unless the task explicitly concerns that configuration.

Start with https://learn.chatgpt.com/docs/prompting and
https://learn.chatgpt.com/docs/build-skills. Discover model-specific guidance via
https://developers.openai.com/api/llms.txt and
https://developers.openai.com/codex/llms.txt. The older Codex cookbook prompting
guide may be useful historically; it is not a universal rule for later models.
