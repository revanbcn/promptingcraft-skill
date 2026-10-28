# Client compatibility receipt — 2026-10-28

This receipt records a local integration check of the **0.4.0 candidate** Skill,
not a new published OpenAI plugin or an updated production MCP deployment.
Gemini client state and workspace were isolated for its test. The Gemini workspace was
trusted only for the test commands using `GEMINI_CLI_TRUST_WORKSPACE=true`.

## Claude Code 2.1.312: production MCP

A headless Claude Code session used a temporary MCP configuration with
`--strict-mcp-config` and the public Streamable HTTP endpoint
`https://mcp.promptingcraft.com/mcp`. Existing Claude authentication was used;
no persistent client MCP configuration was changed. The CLI reported the server
`connected`, discovered and invoked `search_guidance` using fixed public filters,
and returned `oai-reasoning`, its official source and ledger `29860983`. The tool
result and process completed without error. This verifies connection, discovery and
one tool invocation through Claude Code. It does not verify candidate MCP deployment,
Skill activation in this session, or other clients.

## Gemini CLI 0.66.0

- `gemini skills install <candidate-skill-path> --scope workspace --consent`:
  successful installation in the isolated workspace.
- `gemini skills list --all`: `promptingcraft [Enabled]` discovered. A recursive
  comparison against the source candidate produced no differences.
- `gemini mcp add --scope project --transport http promptingcraft-guidance
  https://mcp.promptingcraft.com/mcp`, followed by `gemini mcp list`: `Connected`.
  The separate documented `httpUrl` JSON recipe also reported `Connected`.
- A headless prompt with the isolated profile exited 41 because the profile had no
  configured authentication method. No credentials were copied and no new account
  or scope was created. **Model activation was not observed.**

These checks establish installation, discovery and connection only. They do not
establish Gemini tool discovery, tool invocation or model activation. The remote
connection reached the existing production MCP, not the candidate's local MCP.

## Cursor Agent CLI

Agent CLI `2026.10.22-27dcf5f` detected the project-local
`promptingcraft-guidance` MCP configuration, but `agent mcp list-tools
promptingcraft-guidance` exited 1 because that server had not been approved.
No shared approval list was changed. Connection, tool discovery, invocation and
Skill activation in Cursor were not established by this check.

Client behavior and server state can change; this receipt is a dated observation,
not a guarantee for every version or environment.
