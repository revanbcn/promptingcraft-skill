# OpenAI plugin submission — PromptingCraft.com (Skill + MCP, 0.3.0)

Status record for the combined plugin: the `promptingcraft` skill with the PromptingCraft.com
guidance MCP server at `https://mcp.promptingcraft.com/mcp` (universal endpoint, no
authentication). The earlier Skills-only draft is kept unchanged as a separate plugin
([historical record](openai-submission.md)).

| Item | State |
| --- | --- |
| Portal draft | https://platform.openai.com/plugins/manage/plugin_asdk_app_6acde71d1ddc81918d6095dba60b6023 , version `0.3.0 · Draft`, organization **DondeGo**, project **Default project** (residency **Global**), developer identity **Individual — ALEKSANDR PROKOFYEV**. The Skills-only draft (0.2.0) is unchanged |
| Release candidate | `promptingcraft-plugin-0.3.0.zip` from `main` b4d6d20 (approved C2 identity, walkthrough MP4 URL), SHA-256 `e94313bd7e6f015f7d4dd8f67d3d1379fed9d9df00671466f6fcf97720604272`; two builds byte-identical. Uploaded with **Reupload draft** on 2026-10-13, replacing the earlier upload (`c52682d7…`) |
| Listing | Display name PromptingCraft.com, C2 icon shown, package name `promptingcraft`, category Developer Tools, website/support/privacy/terms URLs on promptingcraft.com |
| MCP server | `https://mcp.promptingcraft.com/mcp`, universal URL, no authentication; Worker 2da27b63 with the challenge secret |
| Domain verification | **Verified** (portal token served by the Worker at `/.well-known/openai-apps-challenge`) |
| Scan Tools | Rescanned after the RC upload: **"No findings in the latest MCP scan."** Three tools and server instructions imported; definitions match production (record kind `promptingcraft_methodology`) |
| Skill check | `promptingcraft`: **Checks passed** after the RC upload; Findings → Blocking: "No blocking findings to show." |
| Metadata findings | Non-blocking: "The plugin's name or description references another AI assistant, model, or platform." (the listing names Codex, Claude Code and Cursor as target agents) |
| Review information | From the ZIP: all supported countries, 5 positive and 3 negative test cases, release notes, walkthrough https://gitlab.com/revanalex/promptingcraft-skill/-/raw/main/docs/review/demo-0.3.0.mp4 (public, `video/mp4`, 160 s); no reviewer credentials (no authentication) |
| Submit for review | **Ready, not submitted.** The dialog holds six owner attestations (OpenAI Terms and Plugin Guidelines; applicable laws; no money transfers or trades; rights to third-party content; suitable for under-18s; not targeting under-13s); none was checked on the owner's behalf |

## Tool annotations and their justification

The portal shows the annotations the server advertises (`provided_tool_annotations`) and has
no separate justification field; the reasons are recorded here for reviewers.

| Tool | readOnly | destructive | openWorld | idempotent | Why |
| --- | --- | --- | --- | --- | --- |
| `search_guidance` | true | false | false | true | Filters a ledger bundled with the server; no network access, no writes, no state |
| `get_guidance` | true | false | false | true | Returns one bundled record by id; unknown ids return an error; nothing is fetched |
| `check_source_freshness` | true | false | true | true | Fetches one allowlisted public documentation page (open web) and compares its hash; writes nothing except a shared 15-minute cache entry keyed by source id, which changes no user-visible state |

Requirements followed: [Submit plugins](https://developers.openai.com/plugins/deploy/submission)
and [Remote MCP server review requirements](https://developers.openai.com/plugins/deploy/app-review)
(global data residency project, universal MCP URL, five positive and three negative test
cases, annotations that match behavior).

Developed by the dondego.com team.
