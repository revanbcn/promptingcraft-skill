I read both files, and they're identical:

```python
def handle_key(state, key):
    if key == "Enter":
        state["confirmed"] = True
    return state
```

Neither one handles Escape, and neither has a "closed" state or any other interaction beyond Enter confirming. The code doesn't tell me which one you mean.

**Which dialog should I fix: `billing_dialog.py` or `profile_dialog.py`?**

I haven't edited anything. Once you answer, I'll add Escape handling to that dialog and run the unittest command from the README. My plan is to set a `closed` flag on Escape, alongside the existing `confirmed` flag. If your dialogs use a different convention for "closed", tell me.