I haven't edited anything yet. You asked me to settle the target with you first, and the files don't settle it.

`billing_dialog.py` and `profile_dialog.py` are identical. Each has only this `handle_key(state, key)`:

```python
def handle_key(state, key):
    if key == "Enter":
        state["confirmed"] = True
    return state
```

The `tests/` directory is empty. Nothing in the code shows which dialog you mean or how "closed" is represented.

Two questions:

1. **Which dialog should get Escape-to-close?**
   - Billing only
   - Profile only
   - Both

2. **If both, how should I share the code?**
   - Duplicate the two-line change in each file. This is the smallest change, but the files can drift apart.
   - Add a small shared stdlib module, for example `dialog_keys.py`, that both files call.

My recommendation is both dialogs, with the change duplicated. It's a two-line change, and you haven't selected a reuse mechanism. If you expect more dialogs, the shared module is worth it.

I'd follow the existing `Enter` pattern and add `elif key == "Escape": state["closed"] = True`. If your dialog state uses a different key for "closed", such as `open=False` or `dismissed`, tell me. I'd also add a unittest in `tests/` covering Escape, and check that Enter still confirms. I'd run it with the README command.

Once you answer, I'll make the edit.

Optionally, an accessibility audit could follow later. It would cover focus trapping, focus return on close, and ARIA roles. It isn't needed for this fix.