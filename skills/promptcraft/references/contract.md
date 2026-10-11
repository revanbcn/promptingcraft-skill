# Shared task contract and comparison

Keep a compact ledger of atomic requirements, source words and strength. Extract
from the ORIGINAL user discussion, including still-applicable prior grants.
The author's tools/files are not evidence of the executor's environment.

| Classification | Meaning | Final treatment |
| --- | --- | --- |
| EXPLICIT_REQUIRED | Stated goal, constraint, settled choice, criterion or scoped authorization | Preserve meaning and strength |
| EXPLICIT_OPTIONAL | User expressly allows a choice/suggestion | Keep optional; never an acceptance gate |
| INFERRED | Author's plausible preference or assumption | Omit, label context, or offer an optional suggestion |
| UNRESOLVED | Missing or conflicting choice with no deciding authority | Preserve as unknown; ask if it materially blocks correctness/scope/safety |
| FORBIDDEN | Explicit exclusion or prohibited action | Preserve exclusion and scope |

Track goal, facts, decisions, constraints, exclusions, checks and authority.
Quote enough original text to establish scope. A goal is not blanket permission
for every action that could advance it. Mentioning production is not a deploy
grant. User choices govern skill preferences within host security controls.

## Compare in both directions

1. Check that every required/forbidden item survives with the same strength,
   condition, target, quantity and authority.
2. Read every final operative clause, including acceptance/completion sections.
   Link it to its source item or classify it as a new optional suggestion.
3. Check entailment: verifying that a 500 cannot show success tests the requested
   bug. Requiring edit retention on every network failure adds behavior. Requiring
   100% coverage invents a completion gate.
4. Retain real conflicts/unknowns. Do not silently choose removal over retention,
   invent a timeout/shortcut, or choose a CSV empty-file convention.
5. Flag additions, optional strengthening, omissions, contradictions, unauthorized
   external actions and invented completion criteria. Remove unsupported mandates
   or make suggestions visibly optional inside the handoff.

An outside note cannot weaken an inside imperative. "Assume X; implement X" still
requires X. Prefer leaving unnecessary assumptions out. Say "Optional suggestion:
…" inside the prompt; do not repeat that suggestion as acceptance. Formatting and
context discovery can clarify intent without adding outcomes. A check directly
verifying the requested result is faithful decomposition; speculative edge cases
and a required new test framework are different requirements.

Authorized stages may continue without new routine approvals. Carry grants only
within original scope/targets. If merge would trigger an unapproved deploy, hold
that merge while continuing authorized preparation. Do not invent extra process
gates or prohibitions when authority is simply unspecified.

## Optional offline checker

Run `python3 scripts/contract_check.py comparison.json` from the standalone skill
folder. The stdlib script needs no API, model, account or network. In manual
ChatGPT use the same comparison with original text and final clauses.
It does not extract or understand arbitrary prose: an author/reviewer supplies
source-anchored semantic annotations. Review extraction completeness, entailment,
modality, external actions and contradictions against the actual texts.

All final text must be covered in order; whitespace may separate clauses:

```json
{
  "schema_version": 1,
  "original": "Fix Save after a 500. Do not deploy.",
  "requirements": [
    {"id": "goal", "classification": "EXPLICIT_REQUIRED", "quote": "Fix Save after a 500.", "kind": "GOAL"},
    {"id": "deploy", "classification": "FORBIDDEN", "quote": "Do not deploy.", "kind": "AUTHORITY", "actions": ["deploy"]}
  ],
  "final_prompt": "Fix Save after a 500.\nDo not deploy.",
  "clauses": [
    {"text": "Fix Save after a 500.", "modality": "REQUIRED", "supports": ["goal"], "relation": "PRESERVES", "kind": "GOAL"},
    {"text": "Do not deploy.", "modality": "FORBIDDEN", "supports": ["deploy"], "relation": "PRESERVES", "kind": "AUTHORITY"}
  ]
}
```

Kinds: GOAL, CONSTRAINT, AUTHORITY, COMPLETION, CONTEXT, FORMAT. Modalities:
REQUIRED, OPTIONAL, FORBIDDEN, UNRESOLVED, CONTEXT. Relations: PRESERVES,
DECOMPOSES, CLARIFIES, SUGGESTS, CONTRADICTS, NOVEL, FORMAT. DECOMPOSES/CLARIFIES
need a short `reason`; an INFERRED item without a quote also needs one. FORMAT
is only for nonoperative headings/layout. Annotate consequential action clauses
with `external_action` (for example `merge`, `deploy`, `send`, `publish`); the same
action must be sourced to an EXPLICIT_REQUIRED or EXPLICIT_OPTIONAL AUTHORITY
item in `supports` and its `actions` list. An original optional grant stays optional;
labeling a newly authorized action optional cannot manufacture permission.

Exit 0 means structurally clean but **REVIEW_REQUIRED**; 1 means **DRIFT**; 2 means
**INVALID** input. False annotations can fool structural checks. A clean result
never proves semantic preservation; read the actual texts. Ordinary prompt users
do not need to prepare JSON to receive an optimized prompt.
