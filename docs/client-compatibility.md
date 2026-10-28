# Client connection recipes

These are **client configuration recipes**, not native marketplace plugins. The skill
and the optional guidance MCP service are separate: connecting the server exposes
structured guidance tools, but does not install or activate the prompt-authoring
skill. Client features, versions and policies change; review the linked vendor docs.
Do not replace an existing configuration file with the examples below: merge the
server entry into the existing object. The public endpoint requires no API key.

The skill currently targets Codex, Claude Code and Cursor handoffs; installing it
in another host does not imply model-specific recommendations for that host or
that automatic activation works. Consult the skill's applicability and dated
references. No client below is claimed to have run a prompt unless explicitly stated.

## Gemini CLI

Gemini CLI documents [workspace skills and activation consent](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md).
From the target project, install the skill from a reviewed local clone:

```sh
gemini skills install /path/to/promptingcraft-skill/skills/promptingcraft --scope workspace
```

The workspace must be trusted. In an interactive session use `/skills reload`, then
`/skills list`; ask to use PromptingCraft for a Codex or Claude Code handoff and
approve activation when prompted. Gemini CLI 0.66.0 installed the skill into a
separate test workspace on 2026-10-28; its untrusted workspace did not discover it.
Discovery in a trusted session and model activation were not tested.

For optional MCP guidance, merge into `.gemini/settings.json` (see
[Gemini MCP configuration](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md)):

```json
{"mcpServers":{"promptingcraft-guidance":{"httpUrl":"https://mcp.promptingcraft.com/mcp"}}}
```

## OpenCode

[OpenCode skill discovery](https://opencode.ai/docs/skills/) includes the project
`.agents/skills/` directory. Copy the entire `skills/promptingcraft/` directory
there, including its references. This follows the documented format; discovery and
activation have not been tested here.

For guidance, merge this into `opencode.json` as documented in
[OpenCode MCP servers](https://opencode.ai/docs/mcp-servers/):

```json
{"$schema":"https://opencode.ai/config.json","mcp":{"promptingcraft-guidance":{"type":"remote","url":"https://mcp.promptingcraft.com/mcp","enabled":true}}}
```

## Cline

For the guidance service, use Cline's MCP Servers > Configure > Remote Servers,
select **Streamable HTTP**, and enter `https://mcp.promptingcraft.com/mcp`.
Alternatively merge this entry into its MCP settings; `type` is significant:

```json
{"mcpServers":{"promptingcraft-guidance":{"type":"streamableHttp","url":"https://mcp.promptingcraft.com/mcp","disabled":false,"autoApprove":[]}}}
```

See [Cline's MCP documentation](https://github.com/cline/cline/blob/main/docs/mcp/mcp-overview.mdx).
This recipe has not been tested in Cline and does not install the skill.

## Kimi CLI

The documented [Kimi CLI skill paths](https://moonshotai.github.io/kimi-cli/en/customization/skills.html)
include project `.agents/skills/`. Copy the entire `skills/promptingcraft/` tree
there. `/skill:promptingcraft` explicitly loads it. This is a portable skill recipe,
not a Kimi-specific prompting recommendation; installation and activation have not
been tested here. Kimi Code CLI is a separate client: check its
[own skill paths](https://moonshotai.github.io/kimi-code/en/customization/skills).

To configure the guidance service in Kimi CLI, its
[documented MCP command](https://github.com/moonshotai/kimi-cli/blob/main/docs/en/customization/mcp.md) is:

```sh
kimi mcp add --transport http promptingcraft-guidance https://mcp.promptingcraft.com/mcp
kimi mcp list
```

This writes client configuration; review existing entries before running it. This
recipe was not executed here.

## Windsurf / legacy Cascade

For legacy Cascade, merge the following entry into its MCP configuration, following
[the current Cascade documentation](https://docs.devin.ai/desktop/cascade/mcp):

```json
{"mcpServers":{"promptingcraft-guidance":{"serverUrl":"https://mcp.promptingcraft.com/mcp"}}}
```

The documentation distinguishes legacy Cascade from the newer Devin Local agent;
the latter uses different configuration. This recipe is untested and does not install
the skill.

## Check the connection

After adding an entry, use the client's server or tools list and confirm that the
server connects and exposes `search_guidance`, `get_guidance` and
`check_source_freshness`. Run a suitable read-only lookup, and distinguish server
connection from successful invocation. If unavailable, use official documentation
or the bundled dated references; do not assume current guidance. See the
[data boundary](mcp-data-boundary.md) before enabling a remote service.
