# Cursor routing notes

Load only for a Cursor executor (Cursor Agent in the editor, Agents Window, CLI or
cloud). Original summary checked 2026-10-12 from cursor.com/docs; revalidate relevant
pages during use. These dated notes are not a live freshness claim.

- Cursor is a host, not a model. Under Auto, Cursor routes each request to a model
  it selects (Cost, Balance or Intelligence modes), first-party or third-party.
  Treat the executor model as unknown under Auto: use agent/general guidance and do
  not apply Claude, GPT, Gemini or Composer prompting rules. Apply model-specific
  guidance only when the user or evidence names the selected model; Composer is
  Cursor's own model, and no Cursor prompting guide for it is recorded here.
- Cursor documents Agent (edits and runs tools), Plan (clarifying questions,
  codebase research and an editable plan before building), Ask (read-only, in the
  CLI) and Debug modes. For investigation-only or planning work, say so in the task
  text; a mode suggestion is optional unless the user chose one, and a plan is not
  authority to build.
- Agent finds relevant files through its own search; `@` mentions attach files,
  folders, terminals, chats or diffs only when the user knows which matter. Do not
  invent `@` targets, rules, skills or MCP servers the executor may not have.
- Project rules and skills are loaded by Cursor, not by the prompt. Do not assume a
  given rule, skill or Custom Mode is active without evidence; restate any
  requirement the executor must follow.
- Cloud agents and Bugbot run elsewhere with their own settings; a handoff for
  them still carries only the user's granted scope and authorization.

Start with https://cursor.com/docs/agent/prompting,
https://cursor.com/docs/agent/plan-mode and https://cursor.com/docs/models-and-pricing.
Discover other Cursor pages through https://cursor.com/llms.txt. Cursor documentation
is official for Cursor's product behavior only; it is not model prompting guidance.
