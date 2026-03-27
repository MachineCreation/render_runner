# ----------------------------------------------------------------------------
# Render_runner service worker
# Joseph Egan
# 2026-03-27
# Sources: None
# ----------------------------------------------------------------------------
# Description: Class for rr worker

# python imports
from __future__ import annotations

import logging
import time
from typing import ClassVar


class Worker:
    __workers: ClassVar[list["Worker"]] = []

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.__worker_number = len(Worker.__workers) + 1
        self.__is_running = True
        self.__logger = logger or logging.getLogger(__name__)
        Worker.__workers.append(self)

        self.__logger.info(
            "Worker %s initialized. Active workers: %s",
            self.__worker_number,
            len(Worker.__workers),
        )

    @property
    def worker_number(self) -> int:
        return self.__worker_number

    @property
    def is_running(self) -> bool:
        return self.__is_running

    def stop(self) -> None:
        self.__is_running = False
        self.__logger.info("Worker %s marked for shutdown.", self.__worker_number)

    def run_idle_cycle(self, sleep_seconds: float = 2.0) -> None:
        """
        Temporary idle cycle.
        Replace later
        - fetch next pending job
        - claim job
        - execute job
        - update database
        """
        if not self.__is_running:
            self.__logger.info(
                "Worker %s idle cycle skipped because worker is stopped.",
                self.__worker_number,
            )
            return

        self.__logger.debug(
            "Worker %s idle cycle started. Sleeping for %s seconds.",
            self.__worker_number,
            sleep_seconds,
        )
        time.sleep(sleep_seconds)

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