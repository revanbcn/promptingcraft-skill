"""Existing behavior preserves unknown fields for compatibility."""
def validate(payload):
    if not isinstance(payload.get("name"), str):
        raise ValueError("name must be a string")
    return dict(payload)
