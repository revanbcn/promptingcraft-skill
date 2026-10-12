Which dialog should Escape close: `billing_dialog.py` or `profile_dialog.py`?

I read both, and they're identical. Each has only a `handle_key(state, key)` function. On `"Enter"` it sets `state["confirmed"] = True`. Neither handles Escape, and neither has an open or close mechanism. There's also no `tests` directory, so the README's unittest command has nothing to run yet.

There's no shared module between them. If you'd like, I could add a small shared helper that both dialogs use, but that's optional. I can also just edit the one dialog you pick.

I haven't edited anything. Once you tell me which dialog, I'll add the Escape handling. I'd also need to know what "closed" should look like in `state`. With no existing close behavior to match, I'd propose `state["closed"] = True`. Does that work for you? I'd then add a test and run the README's unittest command.