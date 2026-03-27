
from app.Data.Database import Database

DB = Database()

DB.connect()
DB.get_cursor()

curs = DB.cursor

# table_setup = '''
# CREATE TABLE IF NOT EXISTS jobs (
# job_id INTEGER PRIMARY KEY,
#     job_name TEXT NOT NULL,
#     prompt_text TEXT NOT NULL,
#     workflow_template_path TEXT NOT NULL,
#     status TEXT NOT NULL CHECK (status IN (
#     'pending',
#     'queued',
#     'running',
#     'completed',
#     'failed',
#     'aborted'
# )),
#     created_at TEXT NOT NULL,
#     updated_at TEXT NOT NULL,
#     animation_length_seconds INTEGER,
#     output_filename TEXT,
#     remote_output_path TEXT,
#     remote_upload_target TEXT,
#     error_message TEXT
# );'''

# table_setup = '''
# CREATE TABLE IF NOT EXISTS job_resume_state (
#     job_id INTEGER PRIMARY KEY,
#     execution_node_name TEXT NOT NULL,
#     temp_working_path TEXT NOT NULL,
#     current_segment_index INTEGER,
#     total_segments INTEGER,
#     last_completed_segment INTEGER,
#     checkpoint_json TEXT,
#     last_heartbeat_at TEXT,
#     updated_at TEXT NOT NULL,
#     FOREIGN KEY (job_id) REFERENCES jobs(job_id)
# );
# '''

# curs.execute(table_setup)

query = '''
SELECT job_id
FROM jobs
WHERE status NOT IN ('completed', 'failed', 'aborted')
'''
curs.execute(query)
DB.connection.commit()
print(curs.fetchall())
DB.close_connection()