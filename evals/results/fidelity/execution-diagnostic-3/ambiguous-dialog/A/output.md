I haven't edited anything yet. You asked me to settle the target with you first, and the files don't settle it.

`billing_dialog.py` and `profile_dialog.py` are identical. Each has only a `handle_key(state, key)` function that sets `state["confirmed"] = True` on Enter. Neither handles Escape, and `tests/` is empty. Nothing in the code points to one dialog over the other.

**Questions for you**
1. **Which dialog should get Escape-to-close?** Billing, profile, or both?
2. **What should "closes" mean in state?** The only existing state key is `confirmed`. I'd follow the Enter pattern and add `state["closed"] = True` on `"Escape"`. Escape would leave `confirmed` untouched, so it doesn't confirm. Tell me if your callers expect a different key.
3. **Reuse mechanism?** Your options:
   - **(a)** Patch only the chosen dialog with a two-line change. This is my recommendation if you picked one dialog.
   - **(b)** Put `handle_key` in a small shared module that both dialogs import. This avoids duplicating the fix, but it changes the structure of both files.
   - **(c)** Patch both dialogs separately and accept the duplication.

Once you answer, I'll make the change and add a unittest in `tests/`. Then I'll run the README command, `python3 -m unittest discover -s tests -v`.

An accessibility audit of keyboard handling, such as focus trapping and the other keys, would be worth doing later. It isn't needed for this fix.