# PromptCraft local installation and ChatGPT compatibility

Documentation checked on 2026-10-12. This is unreleased `main` integration work;
**v0.1.0 remains the canonical release**. Package metadata retains that version;
it does not identify a new release or certify new release assets.

## Supported route

PromptCraft is a skills-only portable Agent Plugins 1.0.0 package. No MCP server,
app connection, credentials, hooks or external service are required to compose a
prompt. Current guidance needs a usable retrieval tool in the authoring chat;
otherwise the skill reports dated or unavailable guidance.

OpenAI documents plugins in Chat and Work on web, desktop and mobile, and in
Codex on desktop/CLI. Installed bundled skills become available in a **new chat**.
Explicit ChatGPT activation uses `@`; natural-language requests can activate a
relevant installed skill. The IDE extension does not support plugins.
See [Plugins](https://learn.chatgpt.com/docs/plugins) and
[Plugins in ChatGPT](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt).

The [local marketplace procedure](https://developers.openai.com/plugins/build/plugins#install-a-local-plugin-manually)
specifically exposes configured marketplace sources in Work or Codex in the
ChatGPT desktop app. This does **not** prove that an arbitrary local source or a
CLI installation is available in ordinary Chat for a particular account. The
plugin directory is available across plans, but individual availability depends
on plan, region, workspace, role, surface and capability. Workspace upload and
publication have separate permission gates. We have not inspected or changed
this owner's account permissions or published a workspace/public plugin.

## Build once and register the real root

The repository catalog is `.agents/plugins/marketplace.json`, named
`dondego-local`. Its `source.path` is `./dist/promptcraft-plugin`, relative to the
**repository root**, not to `.agents/plugins`. The source directory is generated,
ignored by Git, and complete; there are no symlinks. The only maintained skill is
`skills/promptcraft`. The materializer reuses the same reproducible plugin ZIP as
`scripts/package.py`, validates resources, and refuses unmanaged or locally edited
destinations. Updating the canonical source and running it again refreshes the
snapshot and removes obsolete generated files.

For the owner's existing checkout, these are literal paths, not examples. While
MR !4 is held by GitLab compute quota, the clean checkout uses the reviewed local
installation branch `local/epic4-installed`; remote `main` and the release stay
unchanged. This is local installation, not a merge or release:

```sh
cd /Users/Revan/Projects/promptcraft-skill
python3 scripts/prepare_marketplace.py
python3 scripts/validate.py --marketplace
codex plugin marketplace list --json
```

If `dondego-local` is absent, register **this real root**:

```sh
codex plugin marketplace add /Users/Revan/Projects/promptcraft-skill
codex plugin list --marketplace dondego-local --available --json
codex plugin add promptcraft@dondego-local
codex plugin list --marketplace dondego-local --json
```

If already registered to that root, skip `marketplace add`. If the name belongs to
another source, inspect it and resolve that conflict before replacing anything.
Successful installation readback requires `installed=true` **and** `enabled=true`.
Registration or discovery alone does not mean installed. These commands change
only the named source/plugin through supported Codex tooling; do not replace
`~/.agents/plugins/marketplace.json` or `~/.codex/config.toml` manually.

After canonical source changes, prepare again. In Codex CLI 0.162.1,
`marketplace upgrade` refreshes **Git** sources; it is not the update command for
this local source. Refresh the named installed snapshot using:

```sh
python3 scripts/prepare_marketplace.py
codex plugin remove promptcraft@dondego-local
codex plugin add promptcraft@dondego-local
codex plugin list --marketplace dondego-local --json
```

Start a new session. Compare installed resources with the new package before
claiming an update; same version metadata alone does not prove cache freshness.
This removes only the named generated plugin cache, not the canonical skill or
other installed plugins. In ChatGPT Desktop, use its supported uninstall/install
controls and verify availability again.

To reverse the named CLI integration:

```sh
codex plugin remove promptcraft@dondego-local
codex plugin marketplace remove dondego-local
```

Generated files can be retained or removed as disposable build output. Other
marketplaces, plugins, account connections and project skills are unaffected.

## One-time owner action in ChatGPT Desktop

Computer Use currently rejects access to the installed ChatGPT app with:
`Computer Use is not allowed to use the app 'com.openai.codex' for safety reasons.`
No alternate UI automation, app-storage write or simulated ChatGPT run substitutes
for this missing native evidence. All safe packaging and Codex work can proceed.

With the real local source registered:

1. Open ChatGPT Desktop. In Work or Codex, open **Plugins** and select the
   **DondeGo Local** marketplace source (`dondego-local`).
2. Open **PromptCraft by DondeGo**, check its bundled `promptcraft` skill and
   absence of apps/MCP connections, then install with the plus/install control.
   If already installed, confirm it is enabled. Restart/start a new chat if needed.
3. Open a new ordinary **Chat** conversation in the same account/workspace. Type
   `@`, select **PromptCraft** or its bundled **promptcraft** skill, and ask it to
   prepare a Codex prompt. An actual selectable mention and response are the
   activation evidence; a Codex/Work response does not establish Chat activation.
4. In another new Chat, establish the task decisions normally, then say
   **“Prepare a Codex prompt for this task.”** Confirm previous requirements remain
   in the final single copyable code block. See the validation cases below.

If the local source or skill is absent in that account/surface, record which
step is unavailable. Do not paste SKILL.md repeatedly or claim native success.
An eligible workspace uploader can use **Admin console → intended workspace →
Plugins → Add → Upload plugin** with `dist/promptcraft-plugin-0.1.0.zip` generated
by `python3 scripts/package.py --output dist`, then install it and repeat Chat
checks. This is a separate account/permission route, **not performed here**;
upload/publication is not authorized by the CLI install. No new MCP is needed.
See [upload and permission requirements](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt).

The terminal is needed only for initial local setup and source updates. After a
successful Chat installation, ordinary explicit/implicit prompt requests require
no repeated upload, terminal command or restatement of established decisions.
Account-specific Chat availability and activation remain a manual verification
gate until actually observed.

## Practical acceptance cases

Use the sanitized [native cases](../evals/native/cases.json). They cover an actual
two-turn discussion, explicit invocation, unavailable guidance, missing executor
capabilities, unresolved repository identity, exploratory mode, immutable manifest,
negative activation and no-change. Inspect original task clauses against the final
copyable prompt, not length or the assistant's own claim of preservation.

A complete task may return “The original prompt is already suitable. No material
revision is necessary.” while echoing its original body exactly. A blocking
unresolved choice still requires the deciding question. Asking an explanatory
question must not trigger prompt composition. When the target cannot browse,
author-side retrieval must not be described as target-side current evidence.

See [native validation evidence](../evals/results/native-integration/README.md)
for distinct packaging, Codex, Desktop, ordinary Chat and end-to-end states.
These are authoring/usability tests, not downstream executions or proof of
superiority over an original prompt.

Developed by the dondego.com team.
