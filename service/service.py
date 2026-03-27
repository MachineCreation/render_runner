# -------------------------------------------------------------------------------
# Render_runner service
# Joseph Egan
# 2026-03-27
# Sources: None
# -------------------------------------------------------------------------------
# Description: function that runs the service workers in the background

# Local imports
from app.Data.Database import Database
from service.Worker import Worker
from logs import log_config  # assumed to configure logging as a side effect

# python imports
import logging
import signal


running = True


def handle_shutdown(signum, frame) -> None:
    global running
    running = False


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


def rr_service() -> None:
    logger = logging.getLogger(__name__)
    logger.info("Starting Render_runner service.")

    database = Database(logger=logger)
    worker = Worker(logger=logger)

    try:
        while running and worker.is_running:
            worker.run_idle_cycle(sleep_seconds=2.0)

    except Exception:
        logger.exception("Unhandled exception in Render_runner service loop.")

    finally:
        logger.info("Render_runner service entering shutdown sequence.")
        Worker.shutdown(worker)

        try:
            database.close_connection()
        except Exception:
            logger.exception("Failed to close database connection during shutdown.")

        try:
            database.delete_db_object()
        except AttributeError:
            logger.debug("Database.delete_db_object() not present. Skipping.")
        except Exception:
            logger.exception("Failed during database object cleanup.")

        logger.info("Render_runner service shutdown complete.")


if __name__ == "__main__":
    rr_service()