I haven't edited anything. Which dialog should Escape close: `billing_dialog.py`, `profile_dialog.py`, or both?

The task gave a different path than the one I'm running in. I read both files from `[AUTHOR_WORKSPACE_PATH_REDACTED]`.

The two files are identical. Each has only this:

```python
def handle_key(state, key):
    if key == "Enter":
        state["confirmed"] = True
    return state
```

Enter is the only key handled. Neither file has any state for closing, and nothing in them says what "closes" means. The existing interaction is "Enter sets `state["confirmed"] = True`." So I'd have Escape set a matching flag, probably `state["closed"] = True`, unless you want a different one.

Once you pick the target, there are two ways to do it:
- **Edit in place (my recommendation):** add an `elif key == "Escape"` branch to the chosen dialog or dialogs. The change is one line per file, and the files stay independent.
- **Share a helper:** put the key handling in a common module that both dialogs call. That only makes sense if you want both fixed and expect them to keep the same behavior.

Tell me which approach you want, or leave it to me and I'll go with the in-place edit.

I also haven't read `README.md` yet, so I don't know the exact unittest command. My Bash call was denied, and the README read failed on the path mismatch. I'll read it from the working directory and run the command once you've answered.