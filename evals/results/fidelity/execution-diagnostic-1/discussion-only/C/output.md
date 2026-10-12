# Proposal: stricter validation in `validator.py`

## What I could and couldn't find

- **`validator.py`**: found, 5 lines.
- **`README.md`**: found. It only gives the test command and says the fixture is isolated.
- **`guidance.md`**: not found. A glob of the working directory returned only `validator.py` and `README.md`. I have no (a)-labelled evidence, so nothing below is attributed to guidance.
- **Callers and tests**: none found. The README mentions a `tests` directory, but it isn't in the working directory. I can't say how `validate` is used or what it's tested against.
- I edited nothing and ran nothing.

## Current behavior

Source: (b), `validator.py:1-5`.

- `validate(payload)` checks one thing: `payload.get("name")` must be a `str`. Otherwise it raises `ValueError("name must be a string")` (lines 3-4).
- It returns `dict(payload)`, a shallow copy that keeps every key (line 5).
- The docstring says "Existing behavior preserves unknown fields for compatibility" (line 1).
- So B is today's behavior, and A would be a behavior change.
- Other observations, all (b):
  - `payload` must support `.get`. A non-mapping raises `AttributeError`, not `ValueError`.
  - `name` is not required to be non-empty.
  - A missing `name` fails with the same message as a wrong-typed `name`.
  - No other field is validated.

## Comparison

| | A: reject unknown fields | B: preserve unknown fields |
|---|---|---|
| **Relation to today** | (b) Behavior change. It contradicts the docstring at line 1. | (b) Matches current behavior. |
| **Risks** | (c) Existing callers that send extra keys would start failing, and I can't see any callers to size this. Typos are caught early. Adding a field later means updating the validator first. The error message needs to name the offending keys to be useful. | (c) Typos and unexpected input pass silently. Unvalidated data flows downstream, which matters if a consumer treats the output as trusted. "Stricter" would then have to come from other checks, such as a non-empty `name`, a required-key check, or a type check on `payload`. |
| **Verification ideas** | (c) Test that a payload with an extra key raises `ValueError`. Test that a valid payload still passes. Test the error message and that multiple unknown keys are all reported. Search real callers and sample payloads for extra keys before shipping. | (c) Add a regression test that an extra key survives in the output. Check that the returned dict is a copy and that mutating it doesn't affect the input. If other checks are added, test each one. |

## Unresolved decisions

1. **A or B.** This is open. The user hasn't said which meaning of "stricter" they want. (c) My leaning, and only a leaning: B plus other checks is the lower-risk reading, because the code states compatibility as intent. That depends on callers I couldn't inspect.
2. **Who sends extra fields today?** I have no visibility into callers or tests, so I can't judge the compatibility cost of A.
3. **Does `guidance.md` apply?** The file is missing from the fixture. If it exists elsewhere, I need it supplied before anything is attributed to it.
4. **Middle options.** Examples are an allowlist with a deprecation warning, a `strict=` flag defaulting to today's behavior, or collecting unknown fields under a separate key. Whether any of these is wanted is open.
5. **Scope of "stricter".** This could also mean rejecting an empty `name`, separating "missing" from "wrong type", or raising `ValueError` for non-dict payloads.
6. **Error contract.** Should errors report all problems or only the first, and should the message format stay stable for existing consumers?