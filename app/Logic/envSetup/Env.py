# -------------------------------------------------------------------------------
# Environment setup
# Joseph Egan
# 2026-03-17
# Sources: None
# -------------------------------------------------------------------------------
# Description: quick setup class for environment variables needed for the
# application to run.

# Local imports
from app.Logic.processing.helpers import non_empty

# python imports
from pathlib import Path


class Env:

    required_vars = {
        "db_host": {
            'type': str,
            'prompt': 'Enter Database host',
            'valid_func': non_empty},
        "db_port": {
            'type': int
            },
        "db_name": {
            'type': str,
            'prompt': 'Enter Database name',
            'valid_func': non_empty
            },
        "db_user": {
            'type': str,
            'prompt': 'Enter Database user name',
            'valid_func': non_empty
            },
        "db_password": {
            'type': str,
            'prompt': 'Enter Database password',
            'valid_func': non_empty
            },
        "ssh_host": {
            'type': str,
            'prompt': 'Enter SSH host',
            'valid_func': non_empty
            },
        "ssh_port": {
            'type': int
            },
        "ssh_user": {
            'type': str,
            'prompt': 'Enter SSH user name',
            'valid_func': non_empty
            },
        "ssh_passphrase": {
            'type': str,
            'prompt': 'Enter SSH passphrase',
            'valid_func': non_empty
            },
    }

    def __init__(self, db_host: str,
                 db_port: int,
                 db_name: str,
                 db_user: str,
                 db_password: str,
                 ssh_host: str,
                 ssh_port: int,
                 ssh_user: str,
                 ssh_passphrase: str
                 ):
        self.__db_host = db_host
        self.__db_port = db_port
        self.__db_name = db_name
        self.__db_user = db_user
        self.__db_password = db_password

        self.__ssh_host = ssh_host
        self.__ssh_port = ssh_port
        self.__ssh_user = ssh_user
        self.__ssh_passphrase = ssh_passphrase

    def write_env_file(self, file_path: Path):
        with open(file_path, 'w') as f:
            f.write(f'DB_HOST={self.__db_host}\n')
            f.write(f'DB_PORT={self.__db_port}\n')
            f.write(f'DB_NAME={self.__db_name}\n')
            f.write(f'DB_USER={self.__db_user}\n')
            f.write(f'DB_PASSWORD={self.__db_password}\n')
            f.write(f'SSH_HOST={self.__ssh_host}\n')
            f.write(f'SSH_PORT={self.__ssh_port}\n')
            f.write(f'SSH_USER={self.__ssh_user}\n')
            f.write(f'SSH_PASSPHRASE={self.__ssh_passphrase}\n')

    def delete_self(self):
        del self
