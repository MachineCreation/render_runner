# -------------------------------------------------------------------------------
# workflows
# Joseph Egan
# 2026-03-25
# Sources: None
# -------------------------------------------------------------------------------
# Description: Simple function to get a list of workflow template paths from the
# workflow folder 

# Local imports

# python imports
from pathlib import Path

def get_templates() -> tuple[list[str], Path]:
    current_dir = Path(__file__).resolve().parent

    templates = sorted(
        file.name
        for file in current_dir.iterdir()
        if file.is_file() and file.suffix.lower() == ".json"
    )

    return templates, current_dir
