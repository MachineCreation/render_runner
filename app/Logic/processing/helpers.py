# -------------------------------------------------------------------------------
# helpers
# Joseph Egan
# 2026-03-18
# Sources: None
# -------------------------------------------------------------------------------
# Description: Helper functions

# Local imports

# python imports

def non_empty(value: str):
    if not value.strip():
        raise ValueError("Value cannot be empty")