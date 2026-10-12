I read both files, and I haven't edited anything yet.

`billing_dialog.py` and `profile_dialog.py` are identical. Each has a single `handle_key(state, key)` function that sets `state["confirmed"] = True` on Enter and ignores every other key. Neither file has any open/close or focus handling. The repo has no `tests` directory, so there are no existing tests to run.

Which dialog should get the Escape fix: billing, profile, or both?

I also need to know how "closed" should be represented in `state`. The files don't show a convention, so I'd suggest `state["closed"] = True`. If you'd rather use a different key, such as `state["open"] = False`, tell me.

Once you answer, I'll make the change and add a `tests/` unittest for it. I'll then run `python3 -m unittest discover -s tests -v` and report the results.