# Proposal: stricter validation in `validator.py`

## Existing behavior
`validate(payload)` (validator.py:2-5) does two things:
- It requires `name` to be a `str`, and raises `ValueError` otherwise.
- It returns `dict(payload)`, a shallow copy that keeps every other field. The docstring says this is deliberate, "for compatibility".

Two other facts matter here:
- There is no schema or known-field list. "Unknown" has no definition yet, because only `name` is known.
- The glob found only `validator.py` and `README.md`. There is no `tests/` directory, so no existing tests pin the current behavior. I didn't run anything.

## Comparison

| | A: reject unknown fields | B: preserve unknown fields |
|---|---|---|
| Change | Define an allowed set, starting with `{"name"}`. Raise `ValueError` on any extra key. | Keep current pass-through. Possibly tighten other checks, such as non-dict payloads and key types. |
| Catches | Typos (`nmae`), stale clients, and smuggled or unexpected keys | Nothing new about unknown fields |
| Breaks | Any caller sending extra fields fails. This is a breaking change that can't be seen from this file alone. | Nothing |
| Forward and backward compatibility | Poor. Every new field needs a validator release before any client can send it. | Good. Old validators tolerate new clients. |
| Risk | Outages from rollout ordering. The allowed set can drift from reality. | Typos are silently accepted. Unvalidated data flows downstream, which matters if a consumer trusts or mass-assigns the keys. |
| Fits the docstring | No. The docstring and the intent would have to change. | Yes |

## Middle options, if useful
- **A-lite (warn first):** log or collect unknown keys but still accept them. After a period with no unexpected traffic, flip to reject. This gives the data for A with B's safety.
- **Opt-in strictness:** `validate(payload, strict=False)`. The default is B and new callers choose A. This is cheap, but it leaves two behaviors to maintain.
- **Namespaced extensions:** reject unknown top-level keys but allow an `extra` or `x-` prefix. This is stricter while keeping a sanctioned extension point.

## Verification ideas
Characterization tests should come first, whichever option is chosen:
1. `{"name": "a", "extra": 1}` returns a dict that includes `extra`. This pins the current B behavior.
2. A missing `name`, or a non-string `name`, raises `ValueError`.
3. The returned dict is a copy, so mutating it doesn't affect the input.

For A, add tests for these cases:
- Unknown key raises `ValueError`.
- The error message names the offending key.
- Multiple unknown keys.
- `name`-only payloads still pass.

For A-lite, test that unknown keys are reported but not rejected.

Beyond unit tests, grep or sample real callers and payloads for fields beyond `name`. That is the strongest evidence for whether A is safe. The README command (`python3 -m unittest discover -s tests -v`) would need a `tests/` directory to find anything.

## Unresolved decisions
1. **Allowed fields:** is `name` the only legitimate field, or does the real contract include others? Who owns that list?
2. **Who sends extra fields today:** are there known callers or clients relying on pass-through?
3. **Policy:** is a breaking change acceptable, and if so, with what rollout (warn-first, versioning, or strict flag)?
4. **Error shape:** report the first unknown key or all of them? Is a plain `ValueError` enough?
5. **Scope of "stricter":** should this also cover non-dict payloads (currently `payload.get` raises `AttributeError`), empty `name`, and nested values?
6. **Docstring and contract:** the compatibility promise in the docstring needs updating if A is chosen.

I'd lean toward A-lite as a first step if there are real external callers. If this is a closed internal contract, A with a tests-first rollout is reasonable. That's a suggestion only. No decision has been made, and I made no edits.