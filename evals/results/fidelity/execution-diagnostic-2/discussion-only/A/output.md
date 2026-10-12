## Current behavior (`validator.py`)

- `validate(payload)` checks only that `name` is a `str`. Otherwise it raises `ValueError`.
- It returns `dict(payload)`, a shallow copy. Unknown fields pass through unchanged, and the docstring says this is deliberate, for compatibility.
- It does not check that `payload` is a dict. A non-dict would fail with `AttributeError` on `.get`, not `ValueError`.
- `README.md` points to `tests/`, but the fixture has no `tests` directory. I found no existing tests that pin the current behavior.

## Comparison

| | A: reject unknown fields | B: preserve unknown fields |
|---|---|---|
| Behavior change | Breaking. Any payload with an extra key now raises. | None for valid input. It could be formalized with explicit tests and docs. |
| Main risk | Callers or producers that add fields (newer clients, metadata, versioned schemas) start failing. Rollout order matters. | Typos (`nmae`) and unexpected fields pass silently. Strictness gains are limited. Extra data can flow downstream, for example into storage or logs. |
| Strictness gain | High. It catches typos and schema drift early. | Low. It only tightens the known fields, such as `name` being non-empty or length-limited. |
| Forward compatibility | Poor unless an allowlist or version gate exists. | Good. |
| Needs an allowed-field list | Yes, and it must be kept in sync as the schema grows. | No. |
| Error handling | Needs a clear message naming the offending keys. | Unchanged. |

## Verification ideas

These are proposed tests, not run.

- **Characterization tests first, for both options:**
  - A valid payload with only `name` returns an equal dict.
  - A payload with an extra key currently returns that key (this pins the existing behavior).
  - A non-string or missing `name` raises `ValueError`.
  - The returned dict is a copy, so mutating it doesn't affect the input.
- **For A:**
  - An unknown key raises `ValueError`, and the message lists the key names.
  - Multiple unknown keys are all reported.
  - Known-only payloads still pass.
  - Use a log or dry-run mode first to measure how many real payloads carry extra fields.
- **For B:**
  - Unknown keys of various types, including nested ones, round-trip intact.
  - Optionally, a test that known-field checks still run when unknown keys are present.
- **Both:** decide the non-dict input behavior and test it.

## Possible middle path

A could be softened with an opt-in `strict=False` parameter, a warning-then-reject migration, or a namespaced extension field such as `x_*` that is allowed. The default would stay at B's behavior until consumers are known. This is an option to consider, not a recommendation.

## Unresolved decisions

1. Who produces and consumes these payloads? Do any send fields beyond `name`?
2. What is the intended full field set? A needs it defined, and nothing in this fixture defines one.
3. Is breaking existing callers acceptable? If so, what migration or deprecation period is needed?
4. If A is chosen, should it fail on the first unknown key or report all of them? What error type and message format should it use?
5. If B is chosen, are there any further checks on known fields (empty or whitespace-only `name`, length)?
6. Should non-dict payloads raise `ValueError` rather than `AttributeError`? This is independent of A or B.
7. Should unknown fields be copied deeply or shallowly? Currently they are copied shallowly.
8. Where should the tests live? `tests/` doesn't exist yet, so the README command would currently find nothing to run.

I made no edits and ran no tests. Once you pick a direction, or want the middle path, I can implement it along with the characterization tests.