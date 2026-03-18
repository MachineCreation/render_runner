# -------------------------------------------------------------------------------
# make env
# Joseph Egan
# 2026-03-17
# Sources: None
# -------------------------------------------------------------------------------
# Description: Handles logic for creating .env if needed

# Local imports
from app.Logic.envSetup.checkEnv import check_env
from app.Logic.envSetup.Env import Env

# python imports

def make_env():
    file_path, env_exists = check_env()
    print(file_path)
    if not env_exists:
        var_map = {}
        # Logic to create .env file if not found
        for var in Env.required_vars:
            if var['type'] == str:
             value = input(f"Enter value for {var}: ")
            var_map[var] = value
        env = Env(**var_map)
        env.write_env_file(file_path)

        file_path, env_exists = check_env()
        if env_exists:
            env.delete_self()