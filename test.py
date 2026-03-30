from app.Logic.Jobs.Job import Job
from app.Data.Database import Database
from logs import log_config
from pathlib import Path
from service.service import rr_service
from service.Worker import Worker

# db = Database()

# db.reset_db()
# db.delete_db_object()

rr_service()

