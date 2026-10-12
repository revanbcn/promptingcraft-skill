def handle_key(state, key):
    if key == "Enter":
        state["confirmed"] = True
    return state
