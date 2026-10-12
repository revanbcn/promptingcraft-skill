The prompt text itself wasn't included, so this covers the evidence situation and a safe handoff shape. It isn't a line-by-line edit. I'm not running any underlying task.

## Findings

**1. Don't apply the model Y guide to model X.**
- The executor is Codex with model X named explicitly, so Codex-level guidance applies and X-specific tuning is the open question.
- The synthetic index found an X guide, but it hasn't been read. Y's recommendations are evidence about Y only.
- Treat X's behavior as unestablished until its own guide is read.

**2. Leave out the API-only reasoning parameter.**
- The Codex notes put reasoning effort, tool schemas and system-prompt design with API builders. They say not to put API-only configuration in a handoff to an existing Codex CLI unless the task is about that configuration.
- A prompt line like "set reasoning effort to high" can't change a parameter the executor doesn't control. It would also be an operative clause with no source in your task.
- If you want it kept, mark it inside the prompt as "Optional suggestion (unverified for model X): …". It must not be a requirement or an acceptance check.

**3. Don't claim live or official verification.**
- Evidence status:
  - The fixture (`guidance.md`) is dated 2026-10-10 and synthetic.
  - The Codex notes are dated 2026-10-12.
  - Neither is live-verified, and no network retrieval was available.
  - The X guide is a discovered candidate that hasn't been read, so it counts as unavailable.
- The prompt shouldn't say things like "per the official X guide". If the executor has retrieval, you could let it check X's guide, but that would be a new step. Offer it as optional and don't make it a gate.

**4. Keep the model identity as a fact.**
- Say the executor is Codex running model X, because you stated it.
- Don't add behavioral claims about X, such as "X prefers terse prompts" or "X needs step-by-step reasoning". Nothing read supports them.

**5. Check the standard items.**
- Desired outcome, constraints and non-goals are stated in your own words.
- Authority isn't expanded. Don't add "be autonomous", merge, deploy or publish permissions.
- Checks verify the requested result and don't invent new completion gates.
- Context is self-contained. `guidance.md` and the index aren't given to the executor unless your task needs them.
- Planning is neither forced nor banned.

## Placeholder handoff

Paste the real task into the brackets. Without the actual task text, this is the most I can safely produce.

```
[Your original task, verbatim: desired outcome, constraints, exclusions, authority.]

Context: The executor is Codex using model X. Model-specific tuning for X has not been established; follow the task as written.

Verification: [Direct check of the requested behavior, using commands that exist in your repo.]

Optional suggestion: If your environment lets you consult an official guide for model X, you may. Do not apply guidance written for other models or API-only settings, and don't treat this as a requirement.
```

If you paste the actual prompt, I'll compare it clause by clause against your original intent. If it already preserves the contract and has none of the issues above, I'll tell you no change is needed.