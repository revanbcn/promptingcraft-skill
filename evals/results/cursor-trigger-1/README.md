# Cursor activation eval 1 — 2026-10-12

Cursor CLI (`cursor-agent` 2026.10.01-e373342), default model setting (Auto). Cursor
reported the model as `Composer 2.5 Fast` in every run. Runner:
`scripts/evaluate_triggers_cursor.py` with the same 20 queries as `trigger-1`
(`evals/trigger/queries.json`), 3 runs each, `--mode ask` (read-only), a fresh empty
workspace, and the skill installed for the duration as a user skill at
`~/.cursor/skills/promptcraft` (outside the workspace, so workspace search cannot find
it). A run counts as triggered only when the agent read that `SKILL.md`.

Result (`runs.json`, `summary.json`): 60 valid runs, no host failures. Positive runs
0/30 triggered and negative runs 0/30 triggered, so query passes are train 6/12 and
validation 4/8: every negative passes and every positive fails. Cursor did list the skill
as available when asked. Automatic activation therefore was **not** observed with this
model and host configuration.

Supplementary runs (not part of the 20-query rate):

- `explicit-runs.json` (`explicit-queries.json`, 2 runs each): naming the skill in the
  request ("Use the promptcraft skill to …") loaded it 2/2. A leading `/promptcraft` in
  non-interactive `-p` text loaded it 0/2; slash invocation is an editor/CLI chat-input
  feature and was not exercised interactively.
- `diagnostic-gpt-5.3-codex-runs.json`: the first five positive queries once each with
  `--model gpt-5.3-codex` (reported as Codex 5.3 Medium) loaded the skill 3/5. Activation in
  Cursor depends on the selected model; this is a single diagnostic pass, not a rate.

An earlier attempt with the skill inside the workspace was discarded: the agent found the
skill files by searching the workspace, which is not activation. Loading the packaged
plugin through `--plugin-dir` or `~/.cursor/plugins/local/` was not observed in the CLI in
this session (the skill was not listed); plugin loading in the Cursor editor was not
tested. Raw streams are not committed because they contain local paths.

The skill description was not changed for Cursor: the same description activates
30/30 positive and 0/30 negative runs in Codex (`trigger-1`), and a Cursor-specific edit
would need a new evaluation on both hosts.

## Behavior spot check (`behavior/`)

One Cursor-target request (`behavior/query.txt`, the skill named explicitly so it loads)
ran twice with the same default model. Both answers kept the investigation-only scope,
named all three suspected layers without choosing one, and left the product decision on
one-minute staleness open. Both also added mandatory steps the user did not ask for (a
timed reproduction across several runs and a fixed report format), which this project's
contract counts as fidelity defects. This spot check is not graded and is not a quality
claim for Cursor.
