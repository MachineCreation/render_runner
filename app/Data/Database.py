# -------------------------------------------------------------------------------
# Database
# Joseph Egan
# 2026-03-17
# Sources:
# -------------------------------------------------------------------------------
# Description: Class to grant or deny database access

# Local imports
from app.Logic.processing.exceptions import DatabaseConnectionError

# Python imports
from pathlib import Path
import logging
import sqlite3 as sql

# Required imports
import psycopg as psy


# temporary global vars
DB_PATH = Path("test.db")
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "render_jobs"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_TYPE = "sqlite"


class Database:
    __connection = None
    __cursor = None

    __db_types = {
        "postgresql": [
            "postgresql_connection",
            "postgres_save_job",
            "postgres_find_job"
            ],
        "sqlite": [
            "sqlite_connection",
            "sqlite_save_job",
            "sqlite_find_job"
            ],
    }

    def __init__(self, logger: logging.Logger | None = None):
        self.__logger = logger or logging.getLogger(__name__)

    # --------------
    def connect(self):
        try:
            method_name = self.__db_types.get(DB_TYPE)[0]

            if method_name is None:
                self.__logger.error("Unsupported database type: %s", DB_TYPE)
                return False

            connection_method = getattr(self, method_name)
            self.__logger.info("Attempting database connection using db type: %s", DB_TYPE)

            connection_ok = connection_method()

            if connection_ok:
                self.__logger.info("Database connection established successfully.")
            else:
                self.__logger.error("Database connection attempt failed.")

            return connection_ok

        except Exception:
            self.__logger.exception("Exception during connection dispatch.")
            return False

    # --------------
    def get_cursor(self):
        """
        Return a cursor for the active connection.
        """
        if self.__connection is None:
            self.__logger.warning("Cursor requested without an active database connection.")
            return None

        try:
            self.__cursor = self.__connection.cursor()
            self.__logger.info("Database cursor created successfully.")
            return self.__cursor

        except Exception:
            self.__logger.exception("Failed to create database cursor.")
            return None


    # --------------
    def close_connection(self):
        """
        Close cursor and connection if they exist.
        """
        self.close_cursor()

        if self.__connection is not None:
            try:
                self.__connection.close()
                self.__logger.info("Database connection closed successfully.")
            except Exception:
                self.__logger.exception("Failed to close database connection.")
            finally:
                self.__connection = None
        else:
            self.__logger.info("close_connection called with no active connection.")


    # --------------
    def close_cursor(self):
        """
        Close cursor only.
        """
        if self.__cursor is not None:
            try:
                self.__cursor.close()
                self.__logger.info("Database cursor closed successfully.")
            except Exception:
                self.__logger.exception("Failed to close database cursor.")
            finally:
                self.__cursor = None
        else:
            self.__logger.info("close_cursor called with no active cursor.")


    # --------------
    def get_next_id(self) -> int:
        '''
        query database for next available id
        '''
        # self.connect()
        # self.get_cursor()

        # query = '''
        # SELECT TOP 1 job_id
        # FROM jobs
        # '''

        # self.cursor.execute(query)
        # self.connection.commit()
        # response = self.cursor.fetchone()
        # return response[0] + 1
        return 2178

    # ---------------
    def delete_db_object(self):
        del self


# --------------------------------- routers ----------------------------------
    def save_job(self, job: dict):
        '''
        route to best save job function return None
        '''
        method_name = self.__db_types.get(DB_TYPE)[1]
        method = self.__getattribute__(method_name)
        method(job)


    #----------------------
    def find_job(self, id):
        method_name = self.__db_types.get(DB_TYPE)[2]
        method = self.__getattribute__(method_name)
        method(id)

# --------------------------------- properties -------------------------------
    @property
    def cursor(self):
        return self.__cursor
    
    @property
    def connection(self):
        return self.__connection


# -----------------------------PostgreSQL-------------------------------------
    # ---------------
    def postgresql_connection(self) -> bool:
        """
        Try connecting to PostgreSQL database.
        """
        try:
            self.__connection = psy.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
            )

            if isinstance(self.__connection, psy.Connection):
                self.__logger.info(
                    "PostgreSQL connection created. host=%s port=%s dbname=%s",
                    DB_HOST,
                    DB_PORT,
                    DB_NAME,
                )
                return True

            raise DatabaseConnectionError

        except DatabaseConnectionError:
            self.__logger.error(
                "Database connection does not match PostgreSQL connection type. "
                "DB_TYPE=%s expected=%s actual=%s",
                DB_TYPE,
                psy.Connection,
                type(self.__connection),
            )
            return False

        except Exception:
            self.__logger.exception("Exception in PostgreSQL connection.")
            return False


    #---------------------
    def postgres_save_job(self, job: dict):
        '''
        save job
        '''


    #---------------------
    def postgres_find_job(self, id: int):
        '''
        find job in postgres sql
        '''
        

# ---------------------------------SQLite-------------------------------------
    # ----------------
    def sqlite_connection(self) -> bool:
        """
        Try connecting to SQLite database.
        """
        try:
            self.__connection = sql.connect(DB_PATH)

            if isinstance(self.__connection, sql.Connection):
                self.__logger.info(
                    "SQLite connection created. db_path=%s",
                    DB_PATH
                    )
                return True

            raise DatabaseConnectionError

        except DatabaseConnectionError:
            self.__logger.error(
                "Database connection does not match SQLite connection type. "
                "DB_TYPE=%s expected=%s actual=%s",
                DB_TYPE,
                sql.Connection,
                type(self.__connection),
            )
            return False

        except Exception:
            self.__logger.exception("Exception in SQLite connection.")
            return False


    # ----------------
    def sqlite_save_job(self, job:dict):
        '''
        save new or existing job
        '''
        cols = ", ".join(job.keys())
        col_placeholders = ', '.join('?' for _ in job)
        self.connect()
        self.get_cursor()
        
        # save new job
        response = f'''
        INSERT INTO jobs({cols})
        VALUES ({col_placeholders})
        '''

        self.cursor.execute(
            response,
            tuple(job.values())
        )
        self.connection.commit()
        self.close_cursor()


    # ----------------
    def sqlite_find_job(self, id: int):
        from app.Logic.Jobs.Job import Job

        self.connect()
        self.connection.row_factory = sql.Row
        self.get_cursor()

        query = '''
        SELECT *
        FROM jobs
        WHERE job_id = ?
        '''
        self.cursor.execute(query, (id,))
        response = self.cursor.fetchone()
        self.close_cursor()
        if response:
            return True, Job.from_dict(response)
        return False, None