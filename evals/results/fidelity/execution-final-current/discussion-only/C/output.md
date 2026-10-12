## Current behavior

`validator.py` is the only code file in the fixture. There are no callers and no `tests/` directory. The README names a `unittest discover -s tests` command, but there is nothing for it to discover. I didn't run it.

`validate(payload)` does two things:
- It requires `payload["name"]` to be a `str`. Otherwise it raises `ValueError`.
- It returns `dict(payload)`, a shallow copy that keeps every key. Unknown fields pass through unchanged, and the docstring says this is deliberate, for compatibility.

Two further gaps exist today:
- A non-dict payload fails with `AttributeError` from `.get`, not `ValueError`.
- Nested values are shared with the input, because the copy is shallow.

Because I found no callers, I can't say who depends on unknown fields passing through. That is the main unknown.

## Alternatives

| | A: reject unknown fields | B: preserve unknown fields |
|---|---|---|
| Behavior change | Breaking. Payloads that pass today start raising `ValueError`. | None for valid payloads. Today's behavior becomes an explicit contract. |
| Main risk | Breaks producers that send extra fields, including newer clients talking to an older validator. It also needs a definition of "known", and that list must be kept in sync with the schema. | Typos such as `nmae` go unnoticed. Unvalidated data flows downstream, which could matter if a consumer later trusts those keys (for example mass assignment). |
| Compatibility | Poor for rolling upgrades and forward compatibility. | Good. |
| Strictness gained | High. Catches typos and drift early. | Low, unless combined with a warning or a type check on known fields. |
| Implementation sketch | Compare `payload.keys()` to an allowed set and raise `ValueError` listing the extras. | Keep `dict(payload)`. Optionally log unknown keys, or return them under a separate key or structure. |

A middle option is to preserve unknown fields but report them, either through a warning or a `strict=False` parameter. A rollout can then start in warn mode and move to rejection later. It would still require a default for `strict`.

## Verification ideas

Both options:
- Add a test that a payload with only `name` passes.
- Add tests that a missing or non-string `name` raises `ValueError`.
- Add a test for a non-dict payload. Pin down whether that should be `ValueError` or `TypeError`.

For A:
- A payload with an extra key raises `ValueError`, and the message names the key.
- Several extra keys are all reported.
- Nested unknown keys are covered or explicitly out of scope.

For B:
- A payload with an extra key returns that key and value unchanged.
- The returned dict is a copy, so mutating it doesn't change the input.
- Decide whether to pin nested aliasing, since the shallow copy shares nested objects.

Before choosing, run a characterization pass over any real payloads to count how many today carry unknown fields.

## Unresolved decisions

1. Who calls `validate`, and do any of them send or rely on extra fields? Nothing in this fixture shows this.
2. What is the full set of known fields? Today `name` is the only one checked.
3. Should rejection be all-or-nothing (A), or staged: warn first, then reject?
4. Should unknown fields apply to nested objects as well as the top level?
5. What exception type and message format should callers see? Should non-dict input be normalized?
6. Is the shallow-copy aliasing acceptable?
7. Does the `tests/` directory exist elsewhere, or does it need to be created before any of this can be verified?

I haven't made or implied any decision. I'd resolve question 1 first, because it determines whether A is viable at all.