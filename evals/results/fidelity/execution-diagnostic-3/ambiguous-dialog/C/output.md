I looked at both files before asking. `billing_dialog.py` and `profile_dialog.py` are identical. Each has a `handle_key(state, key)` that sets `state["confirmed"] = True` on Enter. Neither handles Escape, and neither has an existing close behavior I could copy.

Which dialog should I fix: **billing**, **profile**, or both? I haven't edited anything and won't until you answer.

If you pick one, I'll add Escape handling there. The dialog has no close mechanism yet, so I'd set `state["closed"] = True` to mirror how Enter sets `confirmed`. Tell me if you'd rather use a different state key. Then I'll run the unittest command from the README and report the result.