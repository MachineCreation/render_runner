# ----------------------------------------------------------------------------
# Render_runner service worker
# Joseph Egan
# 2026-03-27
# Sources: None
# ----------------------------------------------------------------------------
# Description: Class for rr worker

# Local imports
from app.Data.Database import Database
from app.Logic.Jobs.Job import Job

# python imports
import logging
import time
from typing import ClassVar
import random


class Worker:
    __workers: ClassVar[list["Worker"]] = []

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.__worker_number = len(Worker.__workers) + 1
        self.__is_running = True
        self.__database = Database()
        self.__logger = logger or logging.getLogger(__name__)
        Worker.__workers.append(self)

        self.__logger.info(
            "Worker %s initialized. Active workers: %s",
            self.__worker_number,
            len(Worker.__workers),
        )

# --------------------------------- properties ---------------------------------
    @property
    def worker_number(self) -> int:
        return self.__worker_number

    # ------------------
    @property
    def is_running(self) -> bool:
        return self.__is_running

# --------------------------------- lifecycle ---------------------------------
    def run_idle_cycle(self, sleep_seconds: float = 2.0) -> None:
        """
        run idle cycle polls the database for queued jobs and runs them as
        necessary, sets worker to idle when no jobs are found.
        """
        if not self.__is_running:
            self.__logger.info(
                "Worker %s idle cycle skipped because worker is stopped.",
                self.__worker_number,
            )
            return
        
        job = self.poll_queue()

        if not job:
            self.__logger.debug(
            "Worker %s idle cycle started. Sleeping for %s seconds.",
            self.__worker_number,
            sleep_seconds,
            )
            time.sleep(sleep_seconds)
            return
        
        self.run_job(job)

    #----------------------
    def poll_queue(self) -> Job | None:
        return self.__database.poll_queue()

    #----------------------
    def run_job(self, job: Job) -> Job:
        '''
        temporarily update job status to complete or failed
        '''
        rand = random.randint(0, 9)
        if rand % 2 == 0:
            job.status = 'completed'
        else:
            job.status = 'failed'
        print('Running job...')
        time.sleep(60)
        print('...finished job.')
        job.finished_job(self.__database)

    # ---------------------
    def stop(self) -> None:
        self.__is_running = False
        self.__database.delete_db_object()
        self.__logger.info("Worker %s marked for shutdown.", self.__worker_number)

    # ------------------
    @classmethod
    def shutdown(cls, worker: "Worker") -> None:
        if worker in cls.__workers:
            worker.stop()
            cls.__workers.remove(worker)
            worker.__logger.info(
                "Worker %s shutdown complete. Remaining workers: %s",
                worker.worker_number,
                len(cls.__workers),
            )

    @classmethod
    def shutdown_all(cls) -> None:
        for worker in cls.__workers[:]:
            cls.shutdown(worker)

    @classmethod
    def active_worker_count(cls) -> int:
        return len(cls.__workers)