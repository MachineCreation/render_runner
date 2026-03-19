# -------------------------------------------------------------------------------
# Check Env
# Joseph Egan
# 2026-03-17
# Sources: None
# -------------------------------------------------------------------------------
# Description: checks for .env file in folder and prompts for vars if not found

# Local imports
from app.Logic.processing.exceptions import RootPathError

# python imports
from pathlib import Path


# -------------------
def check_env():

    root_path_name = 'render_runner'
    start_path = Path(__file__).resolve().parent
    print(f'start path: {start_path}')
    project_root = start_path

    # check current directory for root
    if start_path.name != root_path_name:
        project_root = get_project_root(start_path, root_path_name)

    # check if env exists
    return search_for_env(project_root)


# -------------------
def get_project_root(start_path: Path, root_path_name: str):

    # set path tracing start
    current_directory = start_path

    # trace path to render_runner root
    while True:
        if current_directory.name.lower() != root_path_name:
            current_directory = current_directory.parent
            if current_directory.parent == current_directory:
                raise RootPathError(
                    f'could not find root directory {root_path_name}'
                    )
        else:
            return current_directory


# -------------------
def search_for_env(root_path: Path):
    env_file = root_path / '.env'

    # look for .env file
    if env_file.exists():
        return None, True
    return env_file, False
