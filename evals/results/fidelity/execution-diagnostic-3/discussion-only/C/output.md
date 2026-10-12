## Proposal: stricter validation in `validator.py`

**What I read.** The whole module is 5 lines. `validate(payload)` checks only that `payload["name"]` is a `str`, otherwise it raises `ValueError("name must be a string")`. It then returns `dict(payload)`, a shallow copy that keeps every other key. So today, unknown fields pass through unchanged, and the docstring says this is deliberate ("preserves unknown fields for compatibility").

**What I couldn't determine.**
- There are no callers in the fixture.
- The README points to a `tests/` directory, but none exists here, so I found no existing tests.
- I don't know who produces payloads, whether any consumer relies on extra keys, or what "compatibility" refers to.
- A non-dict payload would fail with `AttributeError` on `.get`, not `ValueError`. I'm noting that as current behavior, not as a decision.

### Comparison

| | A: reject unknown fields | B: preserve unknown fields |
|---|---|---|
| Change from today | Behavior change. It needs a known-field allowlist, and only `name` is known today. | Close to a no-op. Stricter checks would apply only to known fields. |
| Main risk | It breaks any producer that sends extra keys, and the error appears at runtime. The allowlist can drift from the real schema. Future additions need a coordinated rollout. | Typos such as `nmae` in an optional field are silently accepted. Unvalidated data flows downstream. If the output is later persisted or forwarded, it could carry unexpected content. |
| Benefit | It catches typos and schema drift early, and the contract is explicit. | It stays compatible with old and new clients. It allows gradual rollout of new fields. |
| Error handling | It must decide whether to report the first unknown field or all of them. | It needs no new error paths. |
| Verification | See below. | See below. |

**Verification ideas (A).**
- Unknown key raises `ValueError`, and the message names the key.
- Payloads containing only `name` still pass.
- Run a log-only pass first, which records the unknown keys seen in real traffic before enforcing.
- Check the error type for several unknown keys at once.

**Verification ideas (B).**
- Characterization tests that pin the current behavior: extra keys survive in the output, the output is a copy rather than the same object, and a missing or non-string `name` raises.
- Add a test that nested values are shared (the copy is shallow), if that matters.
- If stricter checks are added on known fields, test each one.

### Middle options, not chosen
- **Warn, don't reject.** Preserve unknown fields but log them. This gives A's visibility with B's compatibility.
- **Namespaced extensions.** Allow unknown keys only under a prefix such as `x_` and reject the rest.
- **Strict mode flag.** Make `validate(payload, strict=False)` so callers opt in to A.

### Unresolved decisions
1. Which behavior is wanted, A, B, or a hybrid? Nobody has chosen yet.
2. Who are the producers and consumers of these payloads, and do any send or read extra fields?
3. What is the full intended schema? A needs it for the allowlist. Today only `name` is defined.
4. If A is chosen, is there a deprecation or rollout period (warn first, then reject)?
5. Should non-dict payloads raise `ValueError` rather than `AttributeError`? This is a separate stricter-validation question.
6. Should the error report every unknown field or just the first?
7. Should B's output stay a shallow copy, or should it be deep-copied?

I didn't edit any files or run any tests. If you tell me which direction, I can draft the change and tests in a follow-up.