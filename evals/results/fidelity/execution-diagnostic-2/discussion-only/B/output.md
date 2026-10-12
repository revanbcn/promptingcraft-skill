**Files found:** only one `validator.py` (the working directory root), so there's no ambiguity. There are no callers and no `tests/` directory. The README mentions `tests`, but the directory doesn't exist.

## 1. Existing behavior toward unknown fields

- `validator.py:1`: the docstring says existing behavior "preserves unknown fields for compatibility." This states intent, and the code matches it.
- `validator.py:3-4`: the only check is that `payload.get("name")` is a `str`. Any other key is never examined.
- `validator.py:5`: `return dict(payload)` returns a shallow copy with every key kept, known or unknown. Nested values are shared with the input, not copied.

Side effects of the current code:
- A missing `name` is rejected, because `get` returns `None`, which isn't a `str`.
- A non-dict payload would raise `AttributeError` from `.get`, not `ValueError`. This is a side observation.

Not confirmed:
- Which fields are "known". The code only knows `name`, and no schema or list exists.
- Who calls `validate` and whether any of them rely on extra fields passing through. No callers or tests exist in this directory.
- Whether tests exist elsewhere. I can't confirm that from here.

## 2. Comparison

| | A: reject unknown fields | B: preserve unknown fields |
|---|---|---|
| Change from baseline | Breaking. Payloads that pass today would raise `ValueError`. | None for passthrough. It formalizes what the code already does. |
| Catches typos like `nmae` | Yes. | No, unless a separate warning is added. |
| Forward/backward compatibility | Poor. A newer producer sending a new field breaks older validators. | Good. Rolling upgrades are safe. |
| Needs a field list | Yes, and it must be kept in sync. Today that list is just `{"name"}`, which is probably incomplete (assumption). | No. |
| Security and data hygiene | Stops unexpected data from flowing downstream. | Unvetted keys flow into whatever consumes the result. This matters if the output is persisted or splatted into something like `**kwargs`. |
| Main risk | Hidden callers fail in production. | "Stricter" isn't delivered, and bad data persists silently. |

## 3. Verification ideas (not implemented)

**For A:**
- A payload with `name` plus an extra key raises `ValueError`, and the message names the offending key.
- A valid payload with only known fields still passes unchanged.
- A missing or non-string `name` still raises the existing error.
- Check all known callers and fixtures against the new rule before shipping. A dry-run or log-only mode could measure how often unknown fields appear in real traffic.

**For B:**
- A characterization test: unknown keys survive in the output with their values intact.
- The output is a copy, so mutating it doesn't change the input. Nested sharing is a known property.
- Known-field checks stay strict.
- If warnings are added, check that they fire without changing the return value.

**Either way:** add the missing `tests/` directory, since the README's command currently has nothing to discover. Also pin down the non-dict input behavior.

## 4. Proposal

The evidence doesn't support a firm recommendation. The code has one field, no callers, and no tests, so I can't tell who would break under A. If forced to choose, I'd lean toward B plus a lighter strictness step:
- Keep passthrough, since it's the documented contract.
- Tighten what is validated, such as non-dict input, empty names, and type checks on any other known fields.
- Optionally log or warn on unknown keys, and measure before deciding on A.

This is a judgment call, not a conclusion from evidence. A makes sense if this is a closed, single-producer boundary where typos are the real problem.

**Unresolved decisions for you:**
1. By "stricter", do you mean rejecting unknown fields, or stricter checks on known fields?
2. Who are the consumers and producers, and can all of them be updated together? That decides whether A's breaking change is acceptable.
3. What is the complete list of known fields? Is `name` the only one?
4. If A: should it be a hard error, or a warn-then-enforce rollout?
5. If B: should unknown keys pass silently, be logged, or be collected under a separate key?
6. Should non-dict payloads raise `ValueError` instead of `AttributeError`?
7. Where should the tests live, and may they pin the current passthrough behavior?