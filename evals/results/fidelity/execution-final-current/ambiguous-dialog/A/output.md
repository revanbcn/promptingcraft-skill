I haven't edited anything yet. You asked me to settle the target with you first, and the code doesn't settle it.

`billing_dialog.py` and `profile_dialog.py` are identical. Each has one `handle_key(state, key)` that sets `state["confirmed"] = True` on Enter and does nothing for other keys. Neither has an existing close or Escape behavior to copy, and `tests/` is empty.

Two questions:

1. **Which dialog should get the fix?** The options are billing, profile, or both.
2. **How should it be shared?** The options are:
   - **(a)** Add the Escape branch to each chosen file separately. It's a two-line change with no new structure.
   - **(b)** Put the shared handler in a new small module that both dialogs call. That avoids duplicating the logic if you want both fixed.

   If you only want one dialog fixed, I'd go with (a). If you want both, I'd go with (b).

Escape also needs a state convention, because the code has no "closed" flag yet. I'd set `state["closed"] = True` and leave `confirmed` unchanged, mirroring how Enter works. Tell me if you want a different name.

Once you confirm, I'll make the change and add a unittest under `tests/`. I'll run the README command to check it.

An accessibility audit of keyboard handling, such as focus trapping and focus return on close, could be worth doing later. It isn't needed for this fix.