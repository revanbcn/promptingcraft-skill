# Grader prompt (ab-1)

The grader was Claude Sonnet 5.5 (`claude-sonnet-5-5`), run once as a fresh Claude Code
subagent with no earlier context. It could read only the blinded file (labels X01–X20,
each with the user request, the case contract and the output, in seeded shuffled order)
and was told not to open the key, use the network or edit files. Its answer is
`grades.json`; `blind-key.json` maps the labels back to conditions. The prompt, with the
local file path replaced:

> You are a blinded grader. Read only this file: `<blinded outputs file>`. Do not open any
> other file in that scratchpad directory (in particular never open blind_key.json or the
> ab/ folder), do not use the network, do not edit anything.
>
> It contains 20 assistant outputs labeled X01..X20. Each answers a user request asking for
> a coding-agent prompt (or a review of one), and lists a "Contract to check". Grade each
> output strictly against its own contract items only (not style or length). For each
> contract item give PASS or FAIL with a one-line reason quoting the output where possible.
> Then count material defects: an added mandatory requirement with no source in the user
> request (new files, mechanisms, thresholds, gates, policies) counts as a defect even if
> the contract item does not name it explicitly, as does a dropped or weakened requirement,
> a resolved-by-guess unresolved choice, or a lost literal.
>
> Return a JSON array only, one object per label: {"label":"X01","case":"<case id>",
> "items":[{"item":"...","verdict":"PASS|FAIL","reason":"..."}],"material_defects":["..."],
> "overall":"PASS|FAIL"}. overall is PASS only if every item passes and material_defects
> is empty. Be consistent across outputs of the same case.

The blinded file was built with seed 20261012, as `scripts/evaluate_ab.py` now does.
