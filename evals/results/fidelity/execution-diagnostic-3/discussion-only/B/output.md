## What I read

There is one `validator.py`, so there was no ambiguity about which file. The directory holds only it and `README.md`. I found no `tests/` directory (the README's unittest command points at one) and no callers of `validate`. I can't say who depends on it or what they expect.

Current behavior of `validate(payload)`:
- It requires `payload.get("name")` to be a `str`. Otherwise it raises `ValueError("name must be a string")`.
- It returns `dict(payload)`, a shallow copy. **Unknown fields are kept unchanged**, and the module docstring says this is deliberate ("preserves unknown fields for compatibility").
- Nothing else is checked. There is no schema or known-field list, and no check that `payload` is a dict. A non-dict, or `None`, would raise `AttributeError` or `TypeError` rather than `ValueError`. That follows from the code, and I did not run it.
- A missing `name` and a non-string `name` raise the same error.

So B is today's behavior. A would be a behavior change.

## Alternatives

| | A: reject unknown fields | B: preserve unknown fields |
|---|---|---|
| Change needed | Define the set of allowed keys, which is only `name` today, and raise `ValueError` on any other key. | None, or only an explicit pass-through contract plus tests. |
| Main benefit | Catches typos and unexpected input. Strict contract. | Compatible with existing callers and with newer producers that add fields. |
| Main risk | Breaks any caller that sends extra fields. This is a breaking change, and I can't see the callers. The allowlist must be kept in sync with every new field. | Typos like `nmae` are silently accepted. Unvalidated data flows downstream. Whoever consumes the output may trust it too much. |
| Rollout | Needs a migration path, such as warn first and then reject. | None needed. |
| Error handling | Needs a clear message that names the offending keys. Decide whether to report all unknown keys or just the first. | Unchanged. |

## Possible middle path (not a recommendation)
Keep B as the default and add an opt-in strict mode, for example `validate(payload, strict=False)`. Alternatively, log unknown keys as warnings first to measure real usage before choosing A.

## Verification ideas (proposals only, nothing run)
- Pin the current behavior first with characterization tests:
  - A valid payload with extra keys is returned with the extras intact.
  - The output is a copy, so mutating it doesn't affect the input.
  - A missing or non-string `name` raises `ValueError`.
- For A:
  - An extra key raises `ValueError`, and the message names it.
  - A payload with only `name` still passes.
  - Several unknown keys are handled as decided.
  - Behavior for non-dict input is explicit.
- Search every consumer of `validate` outside this fixture for extra keys in real payloads. I couldn't do this here.
- If rollout is phased, test that the warning mode doesn't change the return value.

## Unresolved decisions
1. Who calls `validate`, and do any of them send or rely on extra fields? Nothing in this fixture answers that.
2. Is silently accepting typos a real problem, or is forward compatibility the priority?
3. If A is chosen, is the allowlist just `{"name"}`, and who maintains it as the schema grows?
4. Should A be a hard break, or phased (warn, then reject), or opt-in via a flag?
5. Should rejection report all unknown keys or only the first?
6. Should non-dict payloads raise `ValueError` as part of this change? That is a separate question, but it is easy to bundle in.
7. The README names a `tests/` directory that doesn't exist here. Is it missing from the fixture, or still to be written?