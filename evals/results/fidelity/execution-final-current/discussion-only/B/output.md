## 1. Proposal: A (reject unknown fields) vs B (preserve them)

### Confirmed from the code
- `validator.py` has one function, `validate(payload)`, at lines 2–5.
- It requires `payload.get("name")` to be a `str`. Otherwise it raises `ValueError("name must be a string")`.
- It returns `dict(payload)`, a shallow copy that keeps every key. Unknown fields therefore pass through unchanged today.
- The module docstring says: "Existing behavior preserves unknown fields for compatibility." So B is the current behavior, and the code states that intent.
- `name` is the only field the code knows about. No allowlist or schema exists, so "unknown" has no definition yet.
- **Callers:** a grep of the working directory found no references to `validate` outside its definition. The directory contains only `validator.py` and `README.md`.
- **Tests:** there is no `tests/` directory, even though the README command is `python3 -m unittest discover -s tests -v`. That command would find no tests here. I did not run it, as instructed.
- The shallow copy means nested values are shared with the input.
- A non-dict payload would fail with `AttributeError`, not `ValueError`. That is the same under A and B unless you change it.

### Assumed, not confirmed
- Callers exist outside this fixture, such as services, stored data, or other producers. I can't see them, so I can't say who sends extra fields today.
- The "compatibility" in the docstring refers to older or newer producers sending extra keys, or to downstream consumers reading those keys from the returned dict.
- "Stricter" means unknown-field handling only. It could also mean type checks on more fields or non-dict handling.

### Comparison

| | A: reject unknown | B: preserve unknown |
|---|---|---|
| Change from today | Behavior change. Payloads that pass now would raise. | None, or additive only (for example, stricter checks on known fields). |
| Main risk | Breaks any producer sending extra keys. This includes forward-compatibility cases where a newer sender adds a field. It could fail at runtime with no signal in this repo. | Typos and junk keys pass silently. Extra data flows downstream unvalidated. If the output is persisted or forwarded, that can be a data-quality or security problem such as mass assignment. |
| Definition risk | Needs an explicit allowlist. Today that is `{"name"}`. Any field a caller relies on but the allowlist omits becomes a new failure. | Little. It is the status quo. |
| Error design | Must decide the exception type and message, and whether to list all unknown keys or just the first. | Not applicable. |
| Rollout | Riskier. A warn-only phase would help, but it is a third option beyond A and B. | Safe. |

### Verification ideas
**For A:**
- Add tests for each of these:
  - a payload with only `name` passes;
  - a payload with one extra key raises `ValueError`;
  - a payload with several extra keys reports them all (if that is the chosen design);
  - the existing `name` failure still raises;
  - the input is not mutated.
- Before shipping, find real callers and sample real payloads (logs, stored records) and count how many carry extra keys.

**For B:**
- Add characterization tests that pin the current behavior:
  - extra keys survive in the output;
  - the output is a copy, so top-level mutation doesn't affect the input;
  - nested values are shared (document whether that is intended).
- If you add strictness on known fields, test that unknown fields are still preserved alongside it.

**For both:**
- Create the `tests/` directory the README command expects. It doesn't exist now.

## 2. Unresolved decisions

1. **Who calls `validate`, and what do they send?** I can't see any callers here. If real producers send extra fields, A breaks them. This decides how risky A is.
2. **What does "stricter" mean to you?** If it is only about unknown fields, the choice is A or B. If it also covers other checks, B plus tighter known-field checks becomes possible.
3. **If A, what is the allowlist?** It is currently just `name`. Who owns it, and how does it change when a new field is added?
4. **If A, how should rejection roll out?** The options are hard fail immediately, or log or warn first and then fail. This changes the blast radius and adds work.
5. **If B, is passing unknown data downstream acceptable?** If the returned dict is persisted or forwarded, you may want to document that, or strip fields at a later boundary instead.
6. **Error contract.** Should non-dict input raise `ValueError` rather than `AttributeError`? Should unknown-field errors reuse `ValueError`? Callers that catch `ValueError` would be affected.
7. **Copy depth.** Is a shallow copy enough, or should nested values be isolated? This is independent of A and B but easy to settle at the same time.

I haven't picked A or B. Answering decision 1 would do the most to narrow the choice.