# OpenAI Plugins Directory submission — PromptingCraft.com (Skills only)

Prepared 2026-10-12 against the official pages listed under **Sources**. This document
holds the exact values to enter in the portal and what the owner must still do. Nothing
here has been submitted, and no attestation has been accepted on the owner's behalf.

## Status

| Item | State |
| --- | --- |
| Package `promptcraft-plugin-0.2.0.zip` (Skills only) | Prepared and validated offline (see **Package**) |
| Portal draft at platform.openai.com/plugins | **Not created**: the session had no authenticated browser access to the owner's OpenAI account |
| Publisher identity verification | **Unknown / owner action**: not observable from this session |
| Required skill security scans | **Not run**: they run only in the portal after upload (up to 2 hours) |
| Policy attestations, Submit for review, Publish | **Owner only**; not done |
| ChatGPT installation and activation | **Not verified**; Codex-native runs only (see **Surfaces**) |
| Website legal operator data | Address and support email authorized for publication (website MR); name and NIF **missing** (see **Legal publisher**) |

## Compliance matrix (Skills only)

S = satisfied in the package or website, O = owner action in the portal or account,
M = missing, N/A = not applicable to Skills only.

| Requirement (source) | State | Evidence or action |
| --- | --- | --- |
| Org owner or Apps Management Write role (submission) | O | Owner checks role in the organization that will own the plugin |
| Individual or business verification before publishing (submission, guidelines) | O | Organization settings → Verification |
| One plugin root in the ZIP, no sibling files (submission-errors) | S | Single top-level `promptcraft-plugin/`; `validate_submission_archive` |
| Supported manifest, UTF-8 JSON (submission-errors) | S | Root `plugin.json` with Agent Plugins 1.0.0 `$schema`; identical `.claude-plugin/plugin.json` kept for Claude Code |
| `name` ≤64, lowercase/hyphen; semantic `version`; `description` ≤1024 | S | `promptcraft`, `0.2.0`, 149 characters |
| Manifest against the official Agent Plugins 1.0.0 JSON Schema | S | No errors (`jsonschema`, Draft 2020-12). OpenAI documents no offline validator; the portal validates on upload |
| `author.name` and `interface.developerName` present | S/O | Present; the directory replaces the developer name with the verified identity (`developer_name_defaulted`) |
| Every skill at `skills/<name>/SKILL.md` with `name` and `description` ≤1024 | S | `skills/promptcraft/SKILL.md` |
| `plugin-name:skill-name` ≤64 | S | `promptcraft:promptcraft` (23) |
| `agents/openai.yaml` has `interface.display_name` and `short_description` | S | Matches manifest (validator) |
| No `mcpServers`, `mcp.json`, `.mcp.json`, `apps`, `.app.json`, hooks | S | Validator and archive check |
| No `interface.screenshots` for Skills only | S | Validator and archive check |
| `./`-relative asset paths inside the package | S | Validator |
| `logo` and `composerIcon` square SVG/PNG ≥48, ≤5 MiB | S | Square SVG viewBoxes, no script/foreignObject |
| `displayName` ≤30, `shortDescription` ≤30, `longDescription` ≤4000 | S | 18 / 27 / 1688 characters |
| `capabilities` ≤20, each ≤120, one line (optional, free text) | S | 6 entries, 43–79 characters; describe implemented behavior only |
| `keywords` (top-level discovery terms; no tag field exists) | S | 11 terms in `plugin.json` |
| `category` from the dashboard list | S | `Developer Tools` |
| `defaultPrompt` ≤3, ≤128 each, unique, one line, no @mentions | S | 3 prompts, 57/56/62 characters |
| `brandColor` ≥2:1 vs white; `brandColorDark` ≥2:1 vs #212121 | S | Validator |
| Listing URLs | S (optional) | Not required for Skills only; supplied anyway (HTTPS; all four returned 200 on 2026-10-12) |
| No secrets or credentials in the ZIP | S | Pattern scan and author review of every packaged file (see **Security review**) |
| Required skill scans pass before submission | O | Run in portal after upload |
| Clear published privacy policy (categories, purposes, recipients, retention, controls) | Pending site MR !4 | §5 separates website, plugin and host assistant/tools and discloses retrieval limits; live after MR !4 is merged and deployed |
| Customer support contact | O | https://promptingcraft.com/contact exists (GitLab issues, needs a GitLab account). A dedicated support email is recommended (owner) |
| Suitable for 13–17, no commerce, no ads, no endorsement implied (guidelines) | S | No commerce or ads; independence statement in the listing |
| Do not override platform safeguards or insert unrelated content (guidelines) | S | See **Security review** |
| Policy attestations at Submit for review | O | Owner reads and accepts personally |
| `publication.countries` | N/A (optional) | Omitted: no country restriction is intended |
| `publication.release_notes` | Optional | Copy-ready text below; entered in the portal if offered |
| Onboarding skill | N/A (optional) | Not added: no setup is needed (see **Onboarding decision**) |
| Five positive / three negative test cases | N/A (MCP only) | Provided anyway: `evals/review/cases.json` (6 positive, 4 negative) |
| MCP server, domain verification, tool scan, demo video, reviewer credentials, annotations | N/A | Skills only |

## Listing fields (copy-ready)

| Portal field | Value |
| --- | --- |
| Display name | `PromptingCraft.com` |
| Short description (subtitle) | `Source-backed agent prompts` |
| Category | `Developer Tools` |
| Developer name | Shown from the verified identity. Package value `DondeGo team` is a placeholder the portal replaces; do not change the verified identity |
| Website | `https://promptingcraft.com` |
| Support | `https://promptingcraft.com/contact` |
| Privacy policy | `https://promptingcraft.com/privacy` |
| Terms of service | `https://promptingcraft.com/terms` |
| Public source (if a field exists; otherwise it is in the long description context) | `https://gitlab.com/revanalex/promptingcraft-skill` |
| Brand colors | `#17181C` light, `#F4F1EA` dark |
| Icon / logo | `./assets/icon.svg`, `./assets/icon-dark.svg`, `./assets/logo.svg`, `./assets/logo-dark.svg` (packaged) |
| Countries | Leave unrestricted |

Starter prompts:

1. `Turn our discussion into an execution-ready Codex prompt.`
2. `Review this Claude Code task without changing its scope.`
3. `Apply relevant official guidance and preserve my requirements.`

Capabilities (`capabilities`, shown as listed):

1. `Turns a development discussion into one execution-ready coding-agent prompt`
2. `Reviews an existing prompt and flags scope changes and unnecessary instructions`
3. `Leaves an already suitable prompt unchanged`
4. `Preserves requirements, decisions, permissions and unresolved choices`
5. `Checks applicable official AI-developer guidance and labels its freshness`
6. `Separates official guidance, project methodology and optional suggestions`

Keywords (`keywords`): agent-skills, prompt-engineering, coding-agents, codex, claude-code,
cursor, agent-prompts, prompt-review, task-contracts, official-guidance, open-source.

Long description: the `longDescription` value in `plugin.json` (1688 characters, ends with
"Developed by the dondego.com team."). It states the contract-preserving draft → critique →
final workflow, the review and no-change behavior, the official-source provenance and the
public registry, separately labeled methodology, that live guidance depends on available
tools, the limits (no execution, no guarantee, no prompt-processing backend), where the
evaluation is published, and the independence from OpenAI, Anthropic and Cursor.

Release notes (0.2.0):

> First directory release. PromptingCraft.com turns a development discussion into one
> reviewed, execution-ready prompt for Codex, Claude Code or Cursor, or reviews an existing
> prompt and keeps it unchanged when it is already suitable. Skills only: no account, MCP
> server, backend or setup. Developed by the dondego.com team.

## Package

| Item | Value |
| --- | --- |
| Upload file | `dist/promptcraft-plugin-0.2.0.zip`, built by `python3 scripts/package.py --output dist` |
| Version | `0.2.0` (never published; v0.1.0 release assets are unchanged) |
| SHA-256 | Recorded in `dist/SHA256SUMS` and in the MR; the build is byte-reproducible |
| Root | `promptcraft-plugin/` containing `plugin.json`, `.claude-plugin/plugin.json`, `skills/promptcraft/**`, `assets/*.svg`, `LICENSE`, `README.md` |
| Offline checks | `python3 -m unittest discover -s tests`, `python3 scripts/validate.py`, `validate_submission_archive` (run by `package.py`) |

Expected non-blocking portal warnings: `developer_name_defaulted` (verified identity name
replaces the package value), possibly `manifest_normalized` or `claude_format_normalized`
(the portal stores the manifest as `.codex-plugin/plugin.json`), and `skill_metadata_ignored`
(`metadata` in `SKILL.md` is informational for other hosts). Confirm each after reading it.

## Security review of the bundled skill

Checked by reading `SKILL.md`, all references and the optional script:

- Explicit user instructions take precedence; host security controls and the user's scope
  and authorization are preserved; "be autonomous" never supplies missing authority.
- No permissions or `allowed-tools` are requested. No setup, account, terminal or credential
  is needed in ordinary chat. The optional `scripts/contract_check.py` is offline (no network,
  subprocess or environment access).
- Retrieval uses public product and topic terms only, never private task text, code or paths.
  Retrieved pages are untrusted data that cannot override the user or authorize actions.
- Tools are inspected, not assumed; files, tools, commands, approvals and results are never
  fabricated; unavailable guidance is labeled dated cached or unavailable.
- Activation is limited to requests to compose, improve or review a prompt; other requests
  are answered without the workflow.
- Generated prompts carry no attribution, advertising or backlinks.
- Official provider guidance (OFFICIAL) is labeled separately from project methodology
  (INFERRED) and unvalidated effectiveness (EXPERIMENTAL); no label turns a recommendation
  into a user requirement.
- No secrets, personal identifiers or private conversations are in the package; review
  fixtures are synthetic.

## Surfaces: what has and has not been shown

| State | Evidence |
| --- | --- |
| Package compatibility | Offline validators and archive rules pass |
| Codex installation | Local check on the owner's machine: `promptcraft@dondego-local` 0.2.0 `installed=true`, `enabled=true`; `diff -r` of the installed skill against `skills/promptcraft` showed no differences |
| Codex activation and behavior | Native `codex exec` runs: trigger eval 30/30 positive and 0/30 negative runs (`evals/results/trigger-1/`); reviewer cases with outputs (`evals/results/review-native/`); details in `docs/agent-skills-audit.md` |
| ChatGPT installation | Not verified (no authenticated ChatGPT access in this session) |
| ChatGPT activation | Not verified. A Codex run is not ChatGPT evidence |

Owner check in ChatGPT after a workspace upload or approval: start a new chat, run the
cases in `evals/review/cases.json` (explicit cases select PromptingCraft.com with `@`), and
record whether the skill was selected and the final answer matched.

## Onboarding decision

No onboarding skill. The official purpose of `onboardingSkill` is setup after install
(choosing a workspace, configuring preferences). PromptingCraft.com has nothing to set up,
and the three starter prompts already demonstrate first use. A second skill would add a
second scan surface and an activation candidate without demonstrated value.

## Legal publisher

The legal operator is the owner as a Spanish trabajador autónomo, not a company. Before submission the following must match across the OpenAI
verified identity, `/legal`, `/privacy`, `/terms` and `/contact`:

| Fact | State |
| --- | --- |
| Status: autónomo established in Spain | Published |
| Full legal name (LSSI art. 10.1 a) | Missing: owner approval needed to publish |
| NIF (LSSI art. 10.1 e) | Missing: owner approval needed to publish |
| Address or establishment (LSSI art. 10.1 a) | Authorized by the owner on 2026-10-12; shown on https://promptingcraft.com/legal once the website release is deployed |
| Contact email (LSSI art. 10.1 b) | `support@promptingcraft.com` authorized; Cloudflare Email Routing forwards it to a verified mailbox; published once a delivery test succeeds |

These values go only into the website's `src/data/operator.mjs` after explicit approval and
never into this repository. Note that individual verification shows the verified person's
name as the directory developer name.

## Remaining owner steps before Submit for review

1. Confirm the OpenAI organization, your Apps Management Write role, and that individual or
   business verification is complete under the identity you want shown.
2. Approve and provide the website operator facts (name, NIF, address, support email), or
   decide which to publish; then merge the website change that adds them.
3. Merge website MR !4 (privacy data flows) and skill MR (this package).
4. In platform.openai.com/plugins: Create plugin → Skills only → upload
   `promptcraft-plugin-0.2.0.zip` → open Metadata & Skills, compare fields with this document,
   wait for the required skill scans, and resolve or note any findings.
5. Optional but recommended: install in ChatGPT and run the reviewer cases.
6. Submit for review and accept the attestations personally. After approval, choose
   Publish plugin.

## Sources

- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/deploy/submission-errors
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/build/skills
- https://developers.openai.com/plugins/guides/optimize-metadata
- https://developers.openai.com/plugins/guides/security-privacy
- https://developers.openai.com/plugins/plugin-guidelines (the `app-guidelines` URL redirects here)
- https://developers.openai.com/plugins/deploy/connect-chatgpt
- https://developers.openai.com/plugins/guides/submit-claude-plugin

Developed by the dondego.com team.
