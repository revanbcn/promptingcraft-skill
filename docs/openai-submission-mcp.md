# OpenAI plugin submission — PromptingCraft.com (Skill + MCP, 0.3.0)

Status record for the combined plugin: the `promptingcraft` skill with the PromptingCraft.com
guidance MCP server at `https://mcp.promptingcraft.com/mcp` (universal endpoint, no
authentication). The earlier Skills-only draft is kept unchanged as a separate plugin
([historical record](openai-submission.md)).

| Item | State |
| --- | --- |
| Portal draft | Created 2026-10-13 in organization **DondeGo**, project **Default project** (residency **Global**), developer identity **Individual — ALEKSANDR PROKOFYEV**: https://platform.openai.com/plugins/manage/plugin_asdk_app_6acde71d1ddc81918d6095dba60b6023 , version `0.3.0 · Draft`. The Skills-only draft (0.2.0) is unchanged |
| Package | `promptingcraft-plugin-0.3.0.zip` from `main` 0023980, SHA-256 `c52682d787fe30f654543347135798fc17ce05513d2451a26eaa53e1fcfc373e` (two builds identical) |
| MCP server | `https://mcp.promptingcraft.com/mcp`, universal URL, no authentication; Worker version 2da27b63 plus the challenge secret |
| Domain verification | **Verified** with the portal's token, served by the Worker at `/.well-known/openai-apps-challenge` |
| Scan Tools | Connected; `search_guidance`, `get_guidance`, `check_source_freshness` and server instructions imported; **"No findings in the latest MCP scan."** |
| Metadata findings | Non-blocking: "The plugin's name or description references another AI assistant, model, or platform." (the listing names Codex, Claude Code and Cursor as target agents) |
| Review information | Imported from the ZIP: all supported countries, 5 positive and 3 negative test cases, walkthrough URL, release notes; no reviewer credentials needed (no authentication) |
| Walkthrough | [docs/review/](review/README.md) |
| Submit for review | Not done; the owner accepts the policy attestations |

Requirements followed: [Submit plugins](https://developers.openai.com/plugins/deploy/submission)
and [Remote MCP server review requirements](https://developers.openai.com/plugins/deploy/app-review)
(global data residency project, universal MCP URL, five positive and three negative test
cases, annotations that match behavior).

Developed by the dondego.com team.
