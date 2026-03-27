# -------------------------------------------------------------------------------
# make env
# Joseph Egan
# 2026-03-17
# Sources: None
# -------------------------------------------------------------------------------
# Description: Handles logic for creating .env if needed

# Local imports
from app.Logic.envSetup.checkEnv import check_env
from app.Logic.processing.validations import input_y_or_n
from app.Logic.processing.validations import input_port, input_string
from app.Logic.envSetup.Env import Env

# python imports
from pathlib import Path
import logging


def setup_env_ui():

    file_path, env_exists = check_env()

    if file_path and not env_exists:
        start_prompt()
        setup = input_y_or_n()

        if setup and file_path:
            make_env(file_path)
            print(f' .env file created at {file_path}')
        if setup and not file_path:
            print('Proper file path not found.')
            print(
                'Please see the example of the proper .env file'
                'in the root directory of this repo render_runner/.env.example'
                'and use the instructions found within to create your own .env'
                'before creating your virtual environment'
                )
        return
    print('.env file found in program root')


# ----------
def make_env(file_path: Path):
    var_map = {}
    # Logic to create .env file if not found
    for var, param in Env.required_vars.items():
        if param['type'] == str:
            value = input_string(
                prompt=param['prompt'],
                valid_func=param['valid_func']
                )
        else:
            value = input_port()
        var_map[var] = value
    env = Env(**var_map)
    env.write_env_file(file_path)

    file_path_check, env_exists = check_env()
    if env_exists and file_path_check:
        logging.getLogger(__name__).info('Environment variables created')
        env.delete_self()


# ----------
def start_prompt():
    # prompt for the user to start the env setup tool
    print('Would you like to run the environment setup?')
    print('If you have not setup the environment before choose Yes/Y')
    print('If you already have an environment setup ready choose No/N')
