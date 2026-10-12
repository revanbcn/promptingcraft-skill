Which dialog should get the Escape fix: `billing_dialog.py`, `profile_dialog.py`, or both?

I've read both files, and they're identical. Each has a `handle_key(state, key)` that sets `state["confirmed"] = True` on Enter. Neither has any close behavior yet, and there's no `tests` directory. Because of that, I can't tell from the code which one you mean, or what "closes the way it already closes" should look like. I haven't edited anything.

Once you pick, I'll make the change. I'll also ask what "closed" should look like in state, since nothing in either file defines it. One option is a `state["closed"] = True` flag set on Escape.