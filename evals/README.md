# Behavioral evaluation

`cases.json` has ten original synthetic cases: small bug, authorized implementation,
performance, conflict, unauthorized deployment, unknown tools/model, stale docs,
new model guidance, source injection and a non-trigger. No historical user prompts
or conversations are included. `fixtures/guidance.md` is authored test data, never
claimed as live official guidance.

Optional paired run using an existing authenticated Claude Code subscription:

```sh
python3 scripts/evaluate.py --output /tmp/promptcraft-evals --model sonnet
```

Start with the first three representative cases. Each arm starts a fresh temp
workspace with identical task/source fixture and Read/Skill tool allowance.
With-skill loads the session plugin; without-skill disables skills. Global setting
sources and MCP servers are excluded; no Bash, edit, deploy or external-send tools
are allowed. The executor's target model can remain unknown even when the prompt
author's model is observed. Pin a resolved model ID for repeat comparisons.

Raw traces stay outside Git. Before publishing synthetic prompt outputs, review
for leaked paths, account/session details, private content and hidden reasoning;
publish final visible outputs and compact observed metrics only. Report model ID,
actual skill invocation, constraints lost, acceptance checks, unnecessary questions,
output length, wall time and token/cost data when available. A CLI-reported dollar
estimate is not evidence of a new bill or actual subscription charge.

Classify results separately: deterministic package checks; model-judged/manual
semantic observations; observed host behavior. Self-review is not independent
verification. Three cases don't establish general improvement or better downstream
execution. These tests compose handoffs, not implement fixes in a target repository.
See [recorded results](results/README.md) and [surface status](../docs/verification.md).
