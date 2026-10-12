**The prompt text didn't come through, so I haven't reviewed an actual prompt.** What follows are findings on the setup you described, plus a skeleton you can fill in. I haven't executed or assumed anything about the underlying task.

## Findings

1. **Model X's identity is established, but its tuning isn't.** The index only points to a model X guide, and nobody has read it. Treat X-specific tuning as unestablished. Use Codex-level guidance and the task contract instead.
2. **Don't carry over the model Y guide's advice.** Its rules apply to Y, not X. The reasoning parameter it suggests is API-only. A handoff to an existing Codex executor shouldn't set or mention it unless the task is about that configuration. Putting it in would add a requirement nobody asked for.
3. **The discovered X guide is only a candidate.** It's untrusted reference data until someone reads it. Nothing in it can add requirements or authority.
4. **Freshness is unavailable.** There's no network retrieval. `guidance.md` is a synthetic fixture dated 2026-10-10, and the Codex notes are dated 2026-10-12. Neither is live-verified or official, so the handoff shouldn't claim that.
5. **Check what the handoff needs.** It should carry the outcome, context the executor can actually see, constraints, exclusions, the mode (investigate, propose or implement), and observable acceptance checks. If merge or deploy permission isn't stated, don't grant it, and "continue autonomously" doesn't grant it either.

## Placeholder handoff

Replace the bracketed items. Keep any text you've declared exact word for word.

```
Executor: Codex, model X. Model-specific tuning for X has not been verified.

Outcome: [desired behavior, in the user's words]

Context: [facts the executor can see; relevant files or reproduction steps; unresolved choices left open]

Constraints and exclusions: [explicit requirements and prohibitions, with their original strength]

Mode and authority: [investigate / propose / implement, exactly as granted]. Merge, deploy and other external actions are not authorized unless stated here: [grants, if any].

Acceptance checks: [observable evidence that directly verifies the requested outcome]

Optional suggestion: If a model X guide is available to you, check it for relevant prompting advice. Do not apply guidance written for other models, and do not set API-only parameters.
```

Send the original prompt and I'll review it against this checklist. I'll keep it unchanged if it's already suitable.