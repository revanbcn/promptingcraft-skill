I haven't edited anything yet. I need you to pick the target first.

`billing_dialog.py` and `profile_dialog.py` are identical. Each has only this `handle_key(state, key)`:

```python
def handle_key(state, key):
    if key == "Enter":
        state["confirmed"] = True
    return state
```

Neither file has any Escape handling or a "closed" state, so I can't tell what "its existing interaction" means for closing. Two questions:

1. **Which dialog should get the fix?** Billing, profile, or both?
2. **How should the code be shared?** Options are to implement Escape separately in each file, or to put it in a shared helper that both call. I won't choose for you.

I also need to know what "closed" means in state. The existing code sets `state["confirmed"] = True` on Enter. For Escape I could set `state["closed"] = True`, or `state["confirmed"] = False` plus a closed flag. Tell me which you want, or I'll follow whatever convention you point to.

Once you confirm, I'll make the change and run `python3 -m unittest discover -s tests -v`.

An accessibility audit of the dialogs (focus handling, keyboard paths) could be worth doing later, but it isn't needed for this fix.