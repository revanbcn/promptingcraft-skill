# OpenAI Plugins Directory submission — PromptingCraft.com (Skills only)

State as of 2026-10-12, checked against the official pages listed under **Sources**. The
draft exists in the portal; it has **not** been submitted for review, and no attestation
has been accepted on the owner's behalf.

## Status

| Item | State |
| --- | --- |
| Portal draft | Created 2026-10-12 in organization **DondeGo** under developer identity **Individual — ALEKSANDR PROKOFYEV**: plugin `plugins_6acd4b1ca35c8191b74a336e6e21394c`, version `0.2.0 · Draft`, https://platform.openai.com/plugins/manage/plugins_6acd4b1ca35c8191b74a336e6e21394c |
| Uploaded package | `promptcraft-plugin-0.2.0.zip`, SHA-256 `a9ab97ec42596623876ab4d5bf88306b04ad3314857af6a97d72d28e41e56afc`, built from commit `7ad6444` (byte-reproducible) |
| Publisher verification | Individual verification **Approved** in organization settings; business verification was rejected and is not used |
| Portal metadata check | **Blocking:** "We are not accepting more skills-only submissions at this time." Non-blocking: "The plugin’s name or description references another AI assistant, model, or platform." See **Portal findings** |
| Required skill scan | Started on upload; result recorded under **Portal findings** |
| Submit for review | **Not done.** Blocked by the platform finding above; attestations remain owner-only |
| ChatGPT installation and activation | **Not verified**; Codex-native runs only (see **Surfaces**) |
| Website legal operator data | Published on https://promptingcraft.com (/legal, /privacy, /terms, /contact) on 2026-10-12: legal name, NIF, status, address, support email |
| Support email | `support@promptingcraft.com`: Cloudflare Email Routing rule to the owner's verified mailbox; Cloudflare activity log shows authenticated test messages with status `delivered` (2026-10-12) |

## Portal findings

| Finding | Severity | Assessment |
| --- | --- | --- |
| "We are not accepting more skills-only submissions at this time." | Blocking | A platform intake decision, not a package defect. The guidelines say only that "Skills-only plugins may be subject to additional eligibility requirements for listing in the Directory." No package or metadata change can resolve it; adding an MCP server or app to get around it would be new infrastructure and is out of scope. The draft stays ready for a re-check when OpenAI reopens skills-only intake |
| "The plugin’s name or description references another AI assistant, model, or platform." | Non-blocking | Codex, Claude Code and Cursor are named because they are the target agents the prompts are written for, and the independence statement names OpenAI, Anthropic and Cursor. The plugin guidelines contain no rule against naming compatible tools. Not changed: renaming them would hide what the plugin does and would change the tested skill description |

Expected informational portal notices: `developer_name_defaulted` (the directory shows the
verified identity) and `claude_format_normalized` / `manifest_normalized` (the portal stores
the manifest as `.codex-plugin/plugin.json`). `skill_metadata_ignored` (`metadata` in
`SKILL.md`) is informational.

## Compliance matrix (Skills only)

S = satisfied, O = owner action, B = blocked by the platform, N/A = not applicable.

| Requirement (source) | State | Evidence or action |
| --- | --- | --- |
| Org owner or Apps Management Write role (submission) | S | Upload and draft creation succeeded in organization DondeGo |
| Individual or business verification (submission, guidelines) | S | Individual verification Approved; the upload offered "Individual — ALEKSANDR PROKOFYEV" |
| Public URLs accessible and identifying the same publisher (submission) | S | All four URLs return 200; /legal names the operator Prokofyev Aleksandr (legal-name order), self-employed in Spain, NIF, address and email |
| One plugin root in the ZIP, no sibling files (submission-errors) | S | Single top-level `promptcraft-plugin/`; `validate_submission_archive` |
| Supported manifest, UTF-8 JSON, official Agent Plugins 1.0.0 JSON Schema | S | No schema errors (Draft 2020-12, live schema) for the source and the packaged manifest |
| `name` ≤64, semantic `version`, `description` ≤1024 | S | `promptcraft`, `0.2.0`, 149 characters |
| `author.name` ≤120 (required) and `interface.developerName` ≤80 | S | `Aleksandr Prokofyev` (19); the portal shows Developer "Aleksandr Prokofyev" |
| Every skill at `skills/<name>/SKILL.md`, description ≤1024, `plugin:skill` ≤64 | S | `promptcraft:promptcraft`; `skills-ref validate` valid for source and archive |
| `agents/openai.yaml` display name and short description | S | Match the manifest |
| No MCP, apps, hooks or `interface.screenshots` | S | Validator and archive check |
| `displayName` ≤30, `shortDescription` ≤30, `longDescription` ≤4000 | S | 18 / 27 / 1688 |
| `capabilities` ≤20, each ≤120, one line | S | 6 entries, 43–79 characters |
| `defaultPrompt` ≤3, ≤128, unique, no @mentions | S | 57 / 56 / 62 |
| `category` | S | `Developer Tools` |
| Square `logo` and `composerIcon` (SVG, numeric viewBox) | S | 64×64 viewBox, no script or external references |
| `brandColor` / `brandColorDark` contrast | S | Validator |
| `publication.release_notes` (optional) | S | In the package (text below) |
| `publication.countries` (optional) | S | Omitted on purpose: no country restriction |
| Privacy policy content (guidelines) | S | Categories, purposes, legal bases, recipients (Cloudflare, Google for email), transfers, retention, rights, AEPD |
| Support contact (guidelines) | S | https://promptingcraft.com/contact with `support@promptingcraft.com` |
| No secrets in the package | S | gitleaks: no leaks; no operator name, NIF or address in the skill repository or ZIP |
| Required skill scans pass | See **Portal findings** | Run by the portal |
| Directory intake for skills-only plugins | **B** | Blocking finding above |
| Policy attestations and Submit for review | O | Owner only, after intake reopens |
| MCP review cases, demo video, reviewer credentials | N/A | "Skills-only plugins don't need MCP app review cases or a demo recording" |

## Listing fields (as imported by the portal from the package)

| Field | Value |
| --- | --- |
| Display name | `PromptingCraft.com` |
| Short description | `Source-backed agent prompts` |
| Developer | `Aleksandr Prokofyev` (verified individual; DondeGo is credited only as developer in descriptive text) |
| Package name | `promptcraft` |
| Category | `Developer Tools` |
| Website | `https://promptingcraft.com` |
| Support | `https://promptingcraft.com/contact` |
| Privacy policy | `https://promptingcraft.com/privacy` |
| Terms of service | `https://promptingcraft.com/terms` |
| Brand colors | `#17181C` light, `#F4F1EA` dark |
| Icons | `./assets/icon.svg`, `./assets/icon-dark.svg`, `./assets/logo.svg`, `./assets/logo-dark.svg` |
| Countries | Unrestricted |

The portal offers no editable listing fields for this plugin: every value comes from the
package. A metadata change means a new upload.

Starter prompts:

1. `Turn our discussion into an execution-ready Codex prompt.`
2. `Review this Claude Code task without changing its scope.`
3. `Apply relevant official guidance and preserve my requirements.`

Capabilities:

1. `Turns a development discussion into one execution-ready coding-agent prompt`
2. `Reviews an existing prompt and flags scope changes and unnecessary instructions`
3. `Leaves an already suitable prompt unchanged`
4. `Preserves requirements, decisions, permissions and unresolved choices`
5. `Checks applicable official AI-developer guidance and labels its freshness`
6. `Separates official guidance, project methodology and optional suggestions`

Keywords: agent-skills, prompt-engineering, coding-agents, codex, claude-code, cursor,
agent-prompts, prompt-review, task-contracts, official-guidance, open-source.

Long description: `longDescription` in `plugin.json` (1688 characters, ends with
"Developed by the dondego.com team.").

Release notes (`publication.release_notes`, 0.2.0):

> First directory release. PromptingCraft.com turns a development discussion into one
> reviewed, execution-ready prompt for Codex, Claude Code or Cursor, or reviews an existing
> prompt and leaves it unchanged when it is already suitable. Skills only: no account, MCP
> server, backend or setup. Developed by the dondego.com team.

## Reviewer instructions

The ZIP format rejects `reviewer_instructions`, and the portal shows no field for them for a
skills-only plugin. If a reviewer channel opens, use this text:

> PromptingCraft.com is a skills-only plugin with one skill and no setup, account, MCP
> server or backend. Start a new chat per case and send the turns in
> https://gitlab.com/revanalex/promptingcraft-skill/-/blob/main/evals/review/cases.json
> exactly as written. Positive cases should produce one copyable prompt (or, when the
> request is already complete, the sentence "The original prompt is already suitable. No
> material revision is necessary."); negative cases should get an ordinary answer without
> the workflow. Recorded native Codex results are in `evals/results/review-native/`; they
> are Codex runs, not ChatGPT runs. Live documentation checks depend on the host's tools;
> without them the skill labels guidance as dated cached or unavailable. Public evaluation
> with limits: https://promptingcraft.com/benchmarks

### Reviewer cases (`evals/review/cases.json`, 7 positive, 4 negative)

| Case | Scenario | Expected result | Native Codex result |
| --- | --- | --- | --- |
| P1 | Create a Codex prompt (explicit selection) | One Codex prompt, or no-change with the body echoed | No-change, body echoed |
| P2 | Natural-language, two turns | Turn 2 prompt keeps the agreed columns, reuse, no dependencies, implementation yes / deployment no | As expected |
| P3 | Improve a Claude Code prompt without changing scope | Keeps every requested task, removes duplication, adds no scope | As expected |
| P4 | No-change; unavailable documentation path | Exact no-change sentence; honest freshness label | As expected |
| P5 | Unresolved choice (two repositories) | Neither chosen; asks first; investigation only | As expected |
| P6 | Apply official guidance, keep intent | Constraints kept; optional ideas labeled; guidance and freshness stated | No-change with guidance link and date |
| P7 | Prepare a Cursor agent task (natural language) | One Cursor prompt preserving constraints, or no-change with the body echoed | No-change, body echoed, Cursor guide linked (no freshness date label) |
| N1 | Unrelated question | No activation; plain answer | Not activated |
| N2 | Software topic, not a prompt request | No activation | Not activated |
| N3 | "Run the production migration now" (scope expansion) | No action taken or claimed; prompt keeps the user's own authorization only | As expected |
| N4 | Birthday message | No activation | Not activated |

### Evidence, stated with its limits

Public benchmarks: https://promptingcraft.com/benchmarks. With PromptingCraft.com 8/10
PASS and 3 defects; without it 3/10 PASS and 16 defects (after a disclosed scoring
correction; before it 6/10 and 5, 3/10 and 18). Five synthetic tasks, two runs each, one
generator model in Codex, one grader pass; no downstream implementation was run, so no
superiority of the resulting implementations is shown. The figures are supporting
transparency evidence, not a promise about future results. Activation in Codex: 30/30
expected triggers, 0/30 unwanted (`evals/results/trigger-1/`).

## Package

| Item | Value |
| --- | --- |
| Upload file | `promptcraft-plugin-0.2.0.zip` from `python3 scripts/package.py --output dist` at commit `7ad6444` |
| SHA-256 | `a9ab97ec42596623876ab4d5bf88306b04ad3314857af6a97d72d28e41e56afc` (standalone skill ZIP unchanged: `48b29cb7…d1b`) |
| Version | `0.2.0`; first directory upload. The superseded checksum `b427ae53…` (publisher "DondeGo team") was never uploaded |
| Checks | 111 unit tests; `scripts/validate.py`; `skills-ref validate` (agentskills `69ef37e`) on source and archive; official Agent Plugins 1.0.0 schema; two builds byte-identical and identical to a clean-worktree build; gitleaks; packaged script has no network, subprocess or environment access; SVG assets square without scripts |

## Security review of the bundled skill

- Explicit user instructions take precedence; host security controls and the user's scope
  and authorization are preserved; "be autonomous" never supplies missing authority.
- No permissions or `allowed-tools`; no setup, account, terminal or credential in ordinary
  chat. The optional `scripts/contract_check.py` is offline.
- Retrieval uses public product and topic terms only; retrieved pages are untrusted data.
- Files, tools, commands, approvals and results are never fabricated; unavailable guidance
  is labeled dated cached or unavailable.
- Activation is limited to composing, improving or reviewing a prompt.
- Generated prompts carry no attribution, advertising or backlinks.
- OFFICIAL, INFERRED and EXPERIMENTAL labels stay separate; none turns a recommendation
  into a user requirement.
- No secrets, personal identifiers or private conversations are packaged; fixtures are
  synthetic.

## Surfaces: what has and has not been shown

| State | Evidence |
| --- | --- |
| Package compatibility | Offline validators and archive rules pass; portal accepted the upload and imported every field |
| Codex installation and activation | `promptcraft@dondego-local` installed and enabled; trigger eval 30/30 and 0/30; reviewer cases P1–P7, N1–N4 natively |
| ChatGPT installation and activation | Not verified. The draft page offers no test install (its actions menu has only Download draft ZIP and Delete plugin); a Codex run is not ChatGPT evidence |

## Legal publisher

| Fact | State |
| --- | --- |
| Status: self-employed individual (trabajador autónomo), Spain | Published |
| Legal name, NIF (LSSI art. 10.1 a, e) | Published on /legal, /privacy and /terms; supplied to the website at build time and kept out of both repositories' Git history |
| Address (LSSI art. 10.1 a) | Published |
| Email (LSSI art. 10.1 b) | Published; routing delivery observed in the Cloudflare activity log |
| OpenAI developer identity | Individual — ALEKSANDR PROKOFYEV (portal shows "Aleksandr Prokofyev") |

## Remaining owner steps

1. Wait for OpenAI to reopen skills-only intake (the blocking finding). Re-open the draft
   and confirm the finding is gone; nothing in the package needs to change for it.
2. When unblocked: read the skill scan result, then click Submit for review and accept the
   attestations personally. After approval, choose Publish separately.
3. Optional: once the portal allows a test install, run the reviewer cases in ChatGPT and
   record the results as ChatGPT evidence.

## Sources

- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/deploy/submission-errors
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/build/skills
- https://developers.openai.com/plugins/guides/optimize-metadata
- https://developers.openai.com/plugins/plugin-guidelines

Developed by the dondego.com team.
