## What the code does today

`validator.py` has one rule: `name` must be a `str`, otherwise it raises `ValueError`. It returns `dict(payload)`, a shallow copy, so unknown fields pass through unchanged. The docstring says this is deliberate, for compatibility.

I found no `tests/` directory in the fixture, so nothing pins this behavior down. The README's unittest command would currently find no tests. I haven't run it, as you asked.

Two other gaps are separate from the A/B choice:
- A non-dict payload raises `AttributeError` from `.get`, not `ValueError`.
- A missing `name` and a wrong-typed `name` give the same message.

## Comparison

| | A: reject unknown fields | B: preserve unknown fields (status quo, made explicit) |
|---|---|---|
| Behavior change | Breaking. Any caller sending extra keys starts failing. | None for existing callers. |
| Typos like `nmae` | Caught early. | Pass silently, and a missing `name` still errors. |
| Forward compatibility | Poor. A newer producer adding a field breaks older consumers. | Good. Older consumers tolerate newer producers. |
| Security and hygiene | Stops unexpected data from flowing downstream. | Unvetted keys reach downstream code, which matters if that code spreads or persists the dict. |
| Rollout risk | High. Needs a migration or deprecation path. | Low. |
| Error design | Needs a clear message that lists the offending keys. | Needs a decision on whether to expose the unknown keys at all. |

## Variants worth considering

- **A-lite (warn, then reject):** Log unknown fields now and reject later. This gets A's visibility with B's safety during the transition.
- **B+ (preserve, but separate):** Keep unknown fields but expose them separately (for example as `extras`). Downstream code can then tell which fields were validated.
- **Allowlist plus extension namespace:** Reject unknown top-level keys but allow a designated bucket such as `x_*` or `extras`.

## Verification ideas

Add a `tests/` directory with `unittest` cases, which is what the README command expects.
1. **Characterization tests first, against current code:** valid payload passes, and unknown fields are preserved in the output.
2. **Failure cases:** missing `name`, `name=123`, `name=None`, and a non-dict payload. The last one currently shows the `AttributeError` gap.
3. **Copy semantics:** the returned dict is not the input object. It is a shallow copy, so nested values are still shared.
4. **For A:** unknown keys raise `ValueError`, the message names every offending key, and the known-good cases still pass.
5. **For B or B+:** a round trip that keeps unknown keys, and nothing in the output is dropped or renamed.
6. **Before choosing A:** grep the callers or sample real payloads for fields that would start failing.

## Unresolved decisions

1. Who produces the payloads, and do they control their schema? This decides between A and B.
2. Is the full set of known fields just `name`, or does it need to be declared? A can't be built without that list.
3. Should rejection be silent-fail, a hard error, or warn-then-reject on a timeline?
4. Should the non-dict payload case raise `ValueError` as part of this change, or is that a separate fix?
5. If B+ is chosen, what is the output shape, and does that break the current "return a copy" contract?
6. Should the stricter validation apply to nested values, or only top-level keys?

My lean is to start with characterization tests, then A-lite, with the final choice depending on decision 1. That's a recommendation only, since you haven't made a decision.