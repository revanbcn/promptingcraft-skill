# Reviewer walkthrough (0.3.0)

`demo-0.3.0.mp4` (reviewer URL: the raw file, which plays in a browser without signing in;
the same recording as `demo-0.3.0.gif`, 160 s) was recorded on 2026-10-13 in
an ordinary ChatGPT temporary chat with the PromptingCraft.com guidance server
(`https://mcp.promptingcraft.com/mcp`, production) added as a custom MCP connector, which the
recording shows as "PromptingCraft.com guidance (dev test)". All prompts are the synthetic
reviewer test cases from `plugin.json`; no personal data, history or account details are
shown (the left rail was cropped and every frame was checked).

| Case | Shown | Observed |
| --- | --- | --- |
| P1 OpenAI tool-use guidance for Codex | yes | `search_guidance`: official OpenAI records with sources; both sources checked live and unchanged |
| P2 record `oai-untrusted-data` | yes | `get_guidance`: OFFICIAL / GENERAL record with source, applicability, limits and verification |
| P3 Anthropic evaluations source changed? | yes | `check_source_freshness`: updated (hashes differ), no publication date invented, advises reading the current page |
| N1 arbitrary URL freshness | yes | PromptingCraft.com was not used for the URL; ChatGPT used web search and said the checker supports only its registry |
| N2 run a production migration | yes | Declined; nothing was run or pushed; offered to prepare a prompt instead |
| P4 Claude Code prompt with checked guidance | yes (second segment) | Asked additionally to show a short draft and a critique: guidance retrieved and checked through PromptingCraft.com (both sources unchanged), draft, critique against the stated constraints, final prompt in one code block keeping the single-test scope and no new dependencies. ChatGPT composed this with the MCP tools; the bundled skill is not active in ChatGPT, so the wording is ChatGPT's, not the skill's |
| P5, N3 | no | Not recorded; reproducible from the prompts in `plugin.json` |

This shows MCP tool availability and invocation in ChatGPT. It does not show activation of
the bundled skill in ChatGPT, which has not been observed.

Developed by the dondego.com team.
