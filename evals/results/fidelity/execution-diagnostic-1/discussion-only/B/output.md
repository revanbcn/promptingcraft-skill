## Observed behavior (read from `validator.py`)

- `validate(payload)` checks one thing: `payload.get("name")` must be a `str`. Otherwise it raises `ValueError("name must be a string")`.
- It returns `dict(payload)`, a shallow copy of the whole payload. **Unknown fields are currently accepted and passed through unchanged.** The module docstring says this is deliberate: "Existing behavior preserves unknown fields for compatibility."
- Nothing else is validated. There is no field allowlist and no type checks beyond `name`.

**Not found or not read:**
- `guidance.md` is not in the directory. Only `validator.py` and `README.md` exist, so I used no guidance.
- There is no `tests/` directory. The README's test command would find no tests, and I did not run it.
- I can't see any callers.

**Inferred, not read:**
- Which callers or consumers depend on the passthrough.
- What "stricter" was meant to cover. It could mean unknown fields, type checks on other fields, or required fields.
- What the full set of known fields is. The code only knows `name`.
- Whether `payload` can be a non-dict. `payload.get` would raise `AttributeError` for a non-dict, and that is a separate strictness gap.

## Comparison

| | A: reject unknown fields | B: preserve unknown fields |
|---|---|---|
| Relation to current code | Behavior change. Inputs that pass today would raise. | Matches current behavior, so it adds no strictness for unknown fields. |
| Main risk | Breaks existing callers that send extra fields. Breaks forward compatibility when a newer producer adds fields. Needs a definition of "known", and the code knows only `name`. | Typos such as `nmae` pass silently. Unvalidated data flows downstream. Strictness is only partial. |
| Upside | Catches typos and unexpected input early. The contract is explicit. | Safe for existing and newer producers. Supports gradual rollout. |
| Open sub-questions | Is the error a hard failure for all callers? Is the error message listing the fields acceptable? | Should unknown fields be kept verbatim, or kept in a separate bucket? Should they be logged or warned about? |
| Verification ideas (proposals only) | Unit test that `{"name": "x", "extra": 1}` raises. Test that valid payloads still pass. Search callers and sample real payloads for extra keys before enabling. | Keep or add a test that `{"name": "x", "extra": 1}` returns the extra key. Test that the output is a copy, not the same object. |

A middle path exists, but it's an inference on my part, not something in the code. Keep passing unknown fields through but warn or log on them. Alternatively, run A behind a flag, or in a warn-first mode, then tighten later. This gets observability before any break.

## Proposal

1. Before choosing, find out what "stricter" meant and who calls `validate`. The code can't answer either.
2. Add characterization tests for the current behavior: unknown-field passthrough, a non-string `name`, and a missing `name`. This gives a baseline whichever option is chosen.
3. **Recommendation, not a decision:** if callers can't be audited, B plus a warn-only signal on unknown fields is the lower-risk first step. A is reasonable only if the producers are controlled and can be checked. The code doesn't settle this, so the choice stays open.

## Unresolved decisions

- A or B, or a hybrid (warn first, then reject)?
- Who calls `validate`, and do any rely on extra fields?
- Is the schema closed, or expected to grow? If closed, who owns the known-field list?
- Should "stricter" also include type checks on other fields, required-field checks, or non-dict input handling?
- If A is chosen: should rejection be a `ValueError` listing all unknown keys or just the first? Is there a migration window?
- If B is chosen: should unknown fields be kept at the top level or namespaced? Should they be logged?
- Where do the tests live? The README references `tests/`, but it doesn't exist.