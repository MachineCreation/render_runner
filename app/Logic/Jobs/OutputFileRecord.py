# -------------------------------------------------------------------------------
# Output File Record
# Joseph Egan
# 2026-03-17
# Sources: none
# -------------------------------------------------------------------------------
# Description: class to record output file details

# Local imports

# python imports
from dataclasses import dataclass


@dataclass
class OutputFileRecord:
    file_name: str
    subfolder: str
    output_type: str

    def remote_output_path(self, remote_output_directory: str) -> str:
        base_dir = remote_output_directory.rstrip("/")
        if self.subfolder:
            return f'{base_dir}/{self.subfolder}/{self.file_name}'
        return f'{base_dir}/{self.file_name}'
