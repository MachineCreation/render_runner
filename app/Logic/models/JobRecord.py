# -------------------------------------------------------------------------------
# Job Record
# Joseph Egan
# 2026-03-17
# Sources: none
# -------------------------------------------------------------------------------
# Description: class for recording render jobs and statuses

# Local imports

# python imports
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class JobRecord:
    job_id: str
    prompt_text: str
    workflow_template_path: str
    status: str
    created_at: datetime
    updated_at: datetime
    prompt_id: Optional[str] = None
    output_filename: Optional[str] = None
    remote_output_path: Optional[str] = None
    remote_upload_target: Optional[str] = None
    error_message: Optional[str] = None

    def record_job(self):
        # from models.Database import Database
        pass