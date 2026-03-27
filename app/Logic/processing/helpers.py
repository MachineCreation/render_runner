# -------------------------------------------------------------------------------
# helpers
# Joseph Egan
# 2026-03-18
# Sources: None
# -------------------------------------------------------------------------------
# Description: Helper functions

# Local imports

# python imports
import getpass
import logging

COLOR = {
    "red": 31,
    "green": 32,
    "yellow": 33,
    "orange": '38;5;208',
    "blue": 34,
    "magenta": 35,
    "cyan": 36
}

def non_empty(value: str):
    if not value.strip():
        raise ValueError("Value cannot be empty")
    

# -------------------
def get_user():
    try:
        user = getpass.getuser()
        return user
    except OSError:
        logging.getLogger(__name__).exception("failed to get current user")
        return None


# --------------------
def color_text(text: str, color: str) -> str:
    '''
    "red": 31,
    "green": 32,
    "yellow": 33,
    "orange", '38;5;208',
    "blue": 34,
    "magenta": 35,
    "cyan": 36
    '''
    return f"\033[{COLOR.get(color)}m{text}\033[0m"


# --------------------
def sec_to_min_sec(total_seconds: float) -> dict:
    total_seconds = int(total_seconds)

    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return {
        "minutes": minutes,
        "seconds": seconds
    }