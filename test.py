from app.Logic.Jobs.Job import Job
from app.Data.Database import Database
from logs import log_config
from pathlib import Path

job = Job('job_2', 'test the job id func', Path('test.json'))
db = Database()

job.save_job(db)

db.close_connection()
db.delete_db_object()