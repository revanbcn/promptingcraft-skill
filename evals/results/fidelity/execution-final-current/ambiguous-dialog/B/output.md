I read both files, and I haven't edited anything. `billing_dialog.py` and `profile_dialog.py` are identical. Each has one `handle_key(state, key)` function. It sets `state["confirmed"] = True` on Enter and ignores every other key, so Escape does nothing in either dialog. There's no existing close behavior to copy. The README mentions a `tests` directory, but I found none.

I need two answers before I change anything:

1. **Which dialog should I fix?** Billing, profile, or both?
2. **Do you want a shared mechanism or per-dialog changes?** The two files are identical, so either works.
   - **Shared:** I'd add a small common helper that both dialogs call. It keeps the behavior consistent, but it adds a new module.
   - **Per-dialog:** I'd add an Escape branch inside each selected `handle_key`. It's a smaller change, but the logic is duplicated if you pick both.

I also need to know what "closed" should look like in `state`, since nothing defines it. My default would be `state["closed"] = True`, and Escape wouldn't set `confirmed`. Tell me if you want a different key.

Once you answer, I'll write a failing test first. It will send Escape and show the dialog doesn't close. Then I'll make the fix and run `python3 -m unittest discover -s tests -v`.