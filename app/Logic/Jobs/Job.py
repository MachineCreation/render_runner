# -------------------------------------------------------------------------------
# Job
# Joseph Egan
# 2026-03-17
# Sources: none
# -------------------------------------------------------------------------------
# Description: class for recording render jobs

# Local imports
from app.Logic.processing.helpers import get_user, color_text, sec_to_min_sec
from app.Data.Database import Database

# python imports
from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional
from pathlib import Path
import logging


@dataclass
class Job:

    __job_name: str
    __job_id: int | None
    __prompt_text: str
    __workflow_template_path: Path
    __status: str
    __created_at: datetime
    __updated_at: datetime
    __animation_length: Optional[timedelta] = None
    __output_filename: Optional[str] = None
    __remote_output_path: Optional[str] = None
    __remote_upload_target: Optional[str] = None
    __error_message: Optional[str] = None
    # add estimated time to completion
    # estimated render duration 

    def __init__(
            self,
            job_name: str,
            prompt_text: str,
            workflow_template_path: Path,
            length: timedelta | None = None,
            logger: logging.Logger | None = None,
            ):
        self.__job_name = job_name
        self.__job_id = None
        self.__prompt_text = prompt_text
        self.__workflow_template_path = workflow_template_path
        self.__status = 'queued'
        self.__created_at = datetime.now(ZoneInfo("America/Los_Angeles"))
        self.__updated_at = self.__created_at
        self.__logger = logger or logging.getLogger(__name__)

        self.log_job()

        if length is not None:
            self.length = length


# --------------------------------- properties -------------------------------

    @property
    def length(self) -> timedelta | None:
        '''
        optional length used for animation workflows
        '''
        return self.__animation_length

    @length.setter
    def length(self, length: timedelta):
        self.__animation_length = length

    # --------------------
    @property
    def job_id(self):
        return self.__job_id
    
    @job_id.setter
    def job_id(self, value):
        self.__job_id = value
    
    # --------------------
    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status: str):
        self.__status = status

    # --------------------
    @property
    def output_file(self):
        '''
        generated file name for completed generations
        '''
        return self.__output_filename
    
    @output_file.setter
    def output_file(self, filename: str):
        self.__output_filename = filename

    # --------------------
    @property
    def remote_path(self):
        '''
        path to the remote file on remote target
        '''
        return self.__remote_output_path

    @remote_path.setter
    def remote_path(self, path: str):
        self.__remote_output_path = path

    # --------------------
    @property
    def remote_target(self):
        '''
        remote(cloud) upload target
        '''
        return self.__remote_upload_target

    @remote_target.setter
    def remote_target(self, target: str):
        self.__remote_upload_target = target

    # --------------------
    @property
    def error(self):
        '''
        recorded error for failed render jobs
        '''
        return self.__error_message

    @error.setter
    def error(self, message: str):
        self.__error_message = message

# ------------------------------ UI functions ------------------------------
    def log_job(self):
        # from models.Database import Database
        user = get_user()
        self.__logger.info(f'Job {self.__job_id} created by {user}')

    # --------------------
    def print_job(self):
        status_color = ''
        if self.__status == 'running':
            status_color = 'orange'
        elif self.__status  not in ['failed', 'aborted']:
            status_color = 'green'
        else:
            status_color = 'red'
        length_text = str(self.length)
        print(
            f'{color_text(self.__job_name, 'magenta')} | '
            f'{self.__job_id} | '
            f'{color_text(self.__status, status_color)} | '
            f'{color_text(length_text, 'cyan')}')

# --------------------------------- service functions ------------------------
    def save_job(self, db: Database):
        '''
        write the job to the database
        '''
        if self.job_id is None:
            self.job_id = db.get_next_id()
        job = self.to_dict()
        db.save_job(job)

    # --------------------
    def finished_job(
            self,
            db: Database):
        '''
        change job status
        '''
        self.__updated_at = datetime.now(ZoneInfo("America/Los_Angeles"))
        update = db.update_job(self.to_dict())
        return update


# --------------------------------- data conversion --------------------------
    def to_dict(self):
        '''
        convert job object to dict for database storage
        '''
        return {
            'job_name': self.__job_name,
            'job_id': self.__job_id,
            'prompt_text': self.__prompt_text,
            'workflow_template_path': str(self.__workflow_template_path),
            'status': self.__status,
            'created_at': self.__created_at.isoformat(),
            'updated_at': self.__updated_at.isoformat(),
            'animation_length_seconds': self.__animation_length.total_seconds() if self.__animation_length else None,
            'output_filename': self.__output_filename,
            'remote_output_path': self.__remote_output_path,
            'remote_upload_target': self.__remote_upload_target,
            'error_message': self.__error_message
        }

    # --------------------
    @staticmethod
    def from_dict(data: dict):
        '''
        create job object from dict data
        '''
        job = Job(
            job_name=data['job_name'],
            prompt_text=data['prompt_text'],
            workflow_template_path=Path(data['workflow_template_path']),
            length=(None if not data['animation_length_seconds']
                    else timedelta(**sec_to_min_sec(data['animation_length_seconds'])))
        )
        job.__job_id = data['job_id']
        job.__status = data['status']
        job.__created_at = datetime.fromisoformat(data['created_at'])
        job.__updated_at = datetime.fromisoformat(data['updated_at'])
        job.__output_filename = data['output_filename']
        job.__remote_output_path = data['remote_output_path']
        job.__remote_upload_target = data['remote_upload_target']
        job.__error_message = data['error_message']
        return job
