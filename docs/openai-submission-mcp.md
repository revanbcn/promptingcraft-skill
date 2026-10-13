# OpenAI plugin submission — PromptingCraft.com (Skill + MCP, 0.3.0)

Status record for the combined plugin: the `promptingcraft` skill with the PromptingCraft.com
guidance MCP server at `https://mcp.promptingcraft.com/mcp` (universal endpoint, no
authentication). The earlier Skills-only draft is kept unchanged as a separate plugin
([historical record](openai-submission.md)).

| Item | State |
| --- | --- |
| Portal draft | Not created yet |
| Package | Built from merged `main`; SHA-256 recorded here after the build |
| Domain verification | Pending the portal's challenge token (served from the Worker secret `OPENAI_APPS_CHALLENGE` at `/.well-known/openai-apps-challenge`) |
| Scan Tools | Pending |
| Submit for review | Not done; owner attestations are owner-only |

Requirements followed: [Submit plugins](https://developers.openai.com/plugins/deploy/submission)
and [Remote MCP server review requirements](https://developers.openai.com/plugins/deploy/app-review)
(global data residency project, universal MCP URL, five positive and three negative test
cases, annotations that match behavior).

Developed by the dondego.com team.
