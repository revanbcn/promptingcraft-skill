I haven't edited anything yet, because I need you to choose the target first.

`billing_dialog.py` and `profile_dialog.py` are identical. Each has a `handle_key(state, key)` that sets `state["confirmed"] = True` on Enter and does nothing for other keys. Neither has a close or Escape path. The `tests/` directory is empty, so nothing tells me which dialog you mean.

Two decisions for you:

1. **Which dialog should get the Escape fix?** Your options are billing, profile, or both.
2. **How should the fix be shared?**
   - **Option A:** Patch only the chosen file, adding an Escape branch that sets `state["closed"] = True`. This matches the Enter handling, and it's my recommendation if you only need one dialog.
   - **Option B:** If you want both dialogs fixed, move the shared logic into a new common module that both files import. That's stdlib only, with no new dependencies, but it adds a file.
   - **Option C:** Apply the same small edit to both files separately. The duplication stays.

I'd also like you to confirm the state key. I'd use `closed`, since the code has no existing convention for it. If you'd rather use another name, such as `dismissed` or `confirmed = False`, tell me.

Once you answer, I'll make the edit and add a unittest in `tests/`. Then I'll run the README command. I won't commit or deploy anything.

Optionally, an accessibility audit of the dialogs would be worth doing later, covering focus handling and keyboard traps. It isn't needed to finish this task.