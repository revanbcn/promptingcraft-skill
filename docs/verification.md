# Verification status

## Status checked 2026-10-28

- The publisher account readback recorded the existing [ChatGPT plugin](https://chatgpt.com/plugins/plugin_asdk_app_6acde71d1ddc81918d6095dba60b6023) as published at version 0.3.0. Anonymous visibility and ordinary-Chat Skill activation were not established by that readback.
- The [GitHub mirror](https://github.com/revanbcn/promptingcraft-skill) returned anonymous HTTP 200; its `main` and the [canonical GitLab `main`](https://gitlab.com/revanalex/promptingcraft-skill) both resolved to `6435b9d528865e6e709f6d6ed6898865260736a4` on this date. This is a dated observation, not an automatic synchronization guarantee.
- Version 0.4.0 is a separate local upgrade candidate, not a replacement for the published package. Package, client activation, MCP deployment and publication remain separate evidence boundaries.

## Historical verification snapshots

The sections below preserve observations from earlier work. Their labels, access limitations and “not submitted” or “unreleased” statements describe those historical checkpoints and do not supersede the dated status above.

## Unreleased 0.3.0 candidate: guidance MCP server and the `promptingcraft` identifier

- Offline: Python tests, project/catalog validators, MCP tests (`npm test` in `mcp/`),
  `skills-ref validate` for the source skill and both ZIPs, reproducible
  `promptingcraft-skill-0.3.0.zip` / `promptingcraft-plugin-0.3.0.zip`.
- Codex, both modes (standalone skill without any server; plugin with the production MCP
  server; MCP failure): [mode regression](../evals/results/mcp-modes-1/README.md).
- Cursor CLI: named activation 2/2 with `promptingcraft`; automatic activation still 0.
- ChatGPT: MCP tools available and invoked through a custom connector; bundled skill
  activation in ChatGPT not observed. Not submitted to any directory.
- Release candidate (main b4d6d20, C2 identity): plugin ZIP SHA-256 `e94313bd…0272`, two builds
  identical; Agent Plugins 1.0.0 schemas (live copies) valid; `skills-ref` valid; gitleaks clean
  (history and package); MCP Inspector 16/16 on production; Codex smoke: plugin with MCP returned
  no-change after `search_guidance`, `get_guidance`, `check_source_freshness`; standalone skill
  (no plugin) gave draft, critique and final and said the guidance tools were unavailable.

## Unreleased 0.2.0 candidate: PromptingCraft.com brand and plugin readiness

- Local offline checks only: 100 tests, project/catalog validators, reproducible
  `promptcraft-skill-0.2.0.zip` / `promptcraft-plugin-0.2.0.zip` builds and the
  generated `./dist/promptcraft-plugin` source pass. The plugin ZIP carries
  `assets/` icons/logos and no bytecode caches. Identifiers stay `promptcraft`.
- The validator checks listing text limits (display name and short description
  at most 30 characters, long description at most 4000), https website/support/
  privacy/terms URLs, `./`-relative square SVG/PNG assets of at least 48 units,
  brand-color contrast (#17181C on white 17.7:1; #F4F1EA on #212121 14.3:1) and
  skill/manifest display consistency.
- Not performed: remote CI, Codex reinstall/refresh, ChatGPT Desktop or Chat
  activation, plugin-directory submission, tag or release. The listing URLs are
  configured, not verified live here.
- Sections below record earlier states and the former display name.

## Unreleased native plugin integration

- 90 offline tests (85 existing + five marketplace behavior tests), project/catalog
  validators, live portable manifest JSON Schema and reproducible packages pass.
- Local catalog `.agents/plugins/marketplace.json` is `dondego-local`; its generated
  `./dist/promptcraft-plugin` source resolves relative to the repository root.
- Codex installed/enabled readback and five genuine installed-plugin activations
  are observed across six scenarios/seven native turns, including actual resume,
  natural-language invocation, negative activation and exact no-change.
- Entire canonical skill and existing 14-case contracts are unchanged from MR !3.
  These new runs test authoring/install usability, not downstream superiority.
- ChatGPT Desktop exists but supported UI access is policy-denied; Desktop install,
  ordinary Chat activation and ChatGPT end-to-end use remain unverified. Current
  official docs support Chat plugins, with local-source/account availability gates.
- [Evidence, costs and limits](../evals/results/native-integration/README.md);
  [exact one-time owner installation](chatgpt-installation.md). No new release.

## Unreleased contract fidelity and native validation

- 85 offline tests, validator and reproducible packages pass. Exact-span/local
  authority/no-change checks remain annotation-assisted, never semantic guarantees.
- Original 14-case definitions/assertions are unchanged. Prior historical drift
  was 3/14; new blind reassessment of those same outputs is 5/14. New diagnostics
  were 3/14, 1/14, 3/14; the materially changed final workflow is 0/14 in one sample.
- Four genuine packaged Codex invocations observed skill-resource use, contract,
  critique/final or no-change, and honest live/dates-only freshness. Latest native
  run uses the final workflow's ZIP. Native model/cost remain unobserved.
- Native ChatGPT app access was denied by Computer Use policy; no simulation counts.
- Six new source-pressure cases and nine final A/B/C executions use matched tools,
  model and fixtures. Artifact checks pass 9/9; two read-only A Bash discovery calls
  violated the wrapper command limit. All task outcomes/clarifications are reviewed
  separately; no general or fresh-guidance superiority is established.
- Review blockers have RED→GREEN regressions; final evidence and remote CI/merge
  gates remain distinct. Recommendation IMPROVE FURTHER; v0.1.0 release unchanged.
- Full results: [fidelity evidence](../evals/results/fidelity/README.md).

## Unreleased quality-1 candidate

- 54 current offline tests pass for contracts, evaluation collection, knowledge
  provenance, freshness, packaging and isolated installs. Project validator and
  reproducible standalone/plugin builds pass. The separate generic skill-creator
  validator was unavailable because local PyYAML is absent; no dependency was
  added merely for that optional check.
- All ten planned and four realistic public cases ran in the final identical
  composition harness on observed author `claude-sonnet-5-5`, 28 final runs plus
  28 disclosed diagnostic runs. Separate fresh-context semantic review finds
  material drift in B 13/14 and C 3/14; no semantic or behavioral guarantee.
- Six matched downstream fixture runs pass common post-run acceptance. The earlier
  discovery-limited pilot is separately recorded; no general downstream advantage
  is established. These fixtures do not exercise real MR/merge/deploy or production.
- Current Codex/manual ChatGPT runtime comparison remains unestablished. Their
  portable resources/install paths and ordinary manual-use form are preserved.
- Live maintenance retrieved all 27 registry documents successfully; original
  content hashes/metadata are the baseline, not provider-document dumps.
- Independent code review found two Important defects (optional external authority
  and mixed-fence extraction). RED→GREEN fixes and a focused follow-up review passed.
  An actually observed system-message type error also has a regression fix.
- Recommendation: **IMPROVE FURTHER**. No release/tag/version change or deployment.
  Remote MR/main CI and merge receipt follow in the mission ledger.

## Canonical v0.1.0 historical receipt

Delivery checks are recorded here before release. Format, packaging, isolated
installation and observed model runtime are separate claims.

| Surface | Format / package | Installation | Runtime |
| --- | --- | --- | --- |
| ChatGPT ordinary chat | Manual instruction context; portable plugin archive | Native directory install not performed | NOT RUN: no supported ordinary-chat testing session established here |
| Codex | Portable Agent Skills directory; portable plugin format | Isolated project copy checked | Observed isolated CLI read/use smoke; last wording refinement not rerun in Codex |
| Claude Code | Portable skill and validated compatibility manifest | Isolated copy and session-only plugin loading | Three paired cases × two iterations plus two targeted reruns; observed assumption-drift limitation |

No global host configuration was changed. No marketplace submission occurred.
21 offline deterministic tests pass for freshness, metadata, packaging and isolated installation.
Skill-creator validation and Claude strict manifest validation pass. The portable
manifest also passed a separately live-fetched Agent Plugins JSON Schema check. Live registry check:
14/14 usable documents fetched; initial baseline captured as metadata only.
Separate-agent review found and verified fixes for truncated HTTP failures,
index truncation and archive links. Ordinary ChatGPT gate: the supported UI
inventory call timed out; no ordinary-chat session could be established here.
Daily schedule ID 4486529 is configured but inactive; no recurring monitoring
or automatic mirroring is active. Public release/CI evidence is in the release receipt. No prompt-quality or downstream execution improvement is claimed.

## Publication readback boundary

New GitLab repository is publicly readable (unauthenticated HTTP 200). GitHub
repository metadata says public through the authenticated owner API, but its
unauthenticated web page, repository API and raw LICENSE returned HTTP 404.
Public accessibility of the GitHub mirror is **BLOCKED / UNVERIFIED** despite
its public configuration. The account/platform visibility condition cannot be
resolved from repository metadata alone; no account changes or new organization
are authorized here. Authenticated branch/tag parity can still be verified.

The daily schedule remains inactive pending verified recurring quota policy.
No public-directory plugin, marketplace approval or production deployment is claimed.
