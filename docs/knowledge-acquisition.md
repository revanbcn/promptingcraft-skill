# Curated official knowledge — 2026-10-12

The portable [knowledge ledger](../skills/promptcraft/references/knowledge.json)
selects **17 recommendations from 14 official OpenAI/Anthropic pages**. Each record
has source title/URL, retrieval date, provider/model scope, practical recommendation,
evidence or limitation, Promptcraft applicability and conflicts with prior guidance.
Records are original short summaries; no provider manual is copied into the skill.

OpenAI coverage: prompt clarity/context, API instruction hierarchy, reasoning
prompting, evaluations, structured outputs, function tools, agent data/authority
boundaries and caching. Anthropic coverage: prompting, exact-model scope/initiative,
long context, skills/progressive disclosure, tools, evaluations, agent/workflow
complexity and Claude Code authoring. Context7 resolved official libraries before
concept-specific queries; actual usable provider Markdown/web pages were inspected.
An old success-criteria URL was unavailable; the living index points to
`test-and-evaluate/develop-tests`. The tool guide redirects to `tool-use/define-tools`.

Additional current managed-agent configuration/workflow pages were inspected, but
their hosted API controls are not needed for this portable assistant. No new agent
service, effort configuration, orchestration or paid API became a requirement.
The selected 2024 agent-design article explicitly warns that its tooling landscape
changed; its simplicity tradeoff is retained as general design advice with that
limitation, rather than treated as current setup documentation.

OFFICIAL marks provenance. GENERAL/MODEL_SPECIFIC mark scope. INFERRED marks our
contract adaptation. EXPERIMENTAL marks unestablished effectiveness. All provider
recommendations are conditional; no article becomes a mandatory prompt rule.
Retrieval date is not publication/update date; distributed notes remain dated.

The most consequential changes are:

- Simple outcome instructions often suit OpenAI reasoning models; examples and
  reasoning recipes need target-specific testing.
- Sonnet 5.5 documents initiative/scope and JSON-reasoning interventions that must
  stay attached to that model/interface. Neither provider supplies a universal
  reasoning recipe, nor a reason to expose hidden reasoning.
- Structured output validates shape, not factual or contractual meaning. The
  offline contract checker deliberately leaves semantic review pending.
- Progressive disclosure preserves context. Cache advice does not justify padding
  an ordinary handoff or claiming total-task savings from cached input alone.
- Evaluation examples/thresholds are not the user's completion criteria. Promptcraft
  cannot quietly promote them into requirements.
