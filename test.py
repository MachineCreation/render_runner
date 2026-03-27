from app.Logic.Jobs.Job import Job
from datetime import timedelta
from logs import log_config
from app.Data.Database import Database

db = Database()
job = Job('job_2', "this is a new job test prompt", "test workflow", database=db)


job.save_job()
# exists, found_job = db.postgres_find_job(job.job_id)

# if exists:
#     found_job.print_job()

db.close_connection()
db.delete_db_object()
