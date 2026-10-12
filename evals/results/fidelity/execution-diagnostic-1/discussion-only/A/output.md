# Proposal: stricter validation in `validator.py`

I made no edits and ran no tests.

## Existing behavior

`validate(payload)` (`validator.py:2-5`) does two things:
- It requires `name` to be a `str`, and raises `ValueError` otherwise.
- It returns `dict(payload)`, a shallow copy that keeps every unknown field. The module docstring says this is deliberate, for compatibility.

Some things the code does not cover:
- A non-dict payload, such as `None` or a list, fails with `AttributeError` on `.get` instead of `ValueError`.
- No allowed-field list exists, so option A would have to define one.
- The README points to `tests/`, but the fixture only contains `validator.py` and `README.md`. There are no existing tests to anchor either option.

## Comparison

| | A: reject unknown fields | B: preserve unknown fields |
|---|---|---|
| Behavior change | Breaking. Payloads that pass today can raise. | None for valid input. Stricter checks apply only to known fields. |
| Main risk | Rejects legitimate callers who send extra fields, such as newer clients, metadata, or forward-compatible producers. Rollout can fail suddenly. | Typos like `nmae` pass silently. Unvalidated data flows downstream, and a downstream consumer may trust it. |
| Needs | An explicit allowlist. Today only `name` is known, so every other field would be rejected. | Nothing new. Optionally add validation for any newly known fields. |
| Error quality | Good. It can name the offending keys. | Typos stay invisible unless you add warnings or logging. |
| Security posture | Stronger against injection of unexpected keys. | Weaker. Mitigate by treating unknown fields as opaque and never acting on them. |
| Rollback | Hard once clients adapt. | Easy. |

## Middle options, not decided

- **A staged rollout.** Start with B plus a warning or log for unknown keys, measure real traffic, then move to A.
- **A `strict` flag.** `validate(payload, strict=False)` keeps the default behavior and lets callers opt in to A.
- **A namespaced extension area.** For example, allow unknown fields only under an `x_` prefix or an `extra` dict.

## Verification ideas

These need a new `tests/` directory, since none exists. The README command is `python3 -m unittest discover -s tests -v`.

1. **Characterization tests for current behavior.** These pin the behavior before any change:
   - A valid payload with extra keys is returned with those keys intact.
   - A non-string `name` and a missing `name` both raise `ValueError`.
   - The returned dict is a copy, so mutating it doesn't affect the input.
2. **For A:**
   - An unknown key raises `ValueError`, and the message names the key.
   - A valid payload with only known keys still passes.
   - Include a case-sensitivity case and a nested-unknown-key case if nesting is in scope.
3. **For B:**
   - Unknown keys round-trip unchanged.
   - Known-field errors still fire when unknown keys are present.
4. **Both:** non-dict payloads should give a clean `ValueError` instead of `AttributeError`. This is independent of A versus B, and the current behavior may be relied on, so confirm before changing it.
5. **Traffic replay.** Before choosing A, run recorded real payloads through a dry-run strict check and count the rejections.

## Unresolved decisions

1. Which fields are legitimately allowed? A needs the full list, and only `name` is known today.
2. Who calls `validate`, and do they send extra fields intentionally? Nothing in this fixture shows that.
3. Is a breaking change acceptable, and if so, with what migration path or deprecation window?
4. Should unknown fields be an error, a warning, or silently kept, and should that be configurable?
5. Should non-dict payloads raise `ValueError`? That would change today's `AttributeError`.
6. Is the "for compatibility" docstring a hard requirement or just history?
7. Do nested objects need the same policy?

My recommendation, if you want one: add the characterization tests first, then ship B with unknown-key logging or an opt-in `strict` flag. Move to A only after traffic data shows that rejecting unknown fields is safe.