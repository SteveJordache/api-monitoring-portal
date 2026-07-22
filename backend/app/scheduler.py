from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select

from app.database import SessionLocal
from app.models import MonitorModel
from app.services import execute_monitor


# One scheduler instance for the FastAPI process.
scheduler = BackgroundScheduler(timezone="UTC")


def run_scheduled_monitor(monitor_id: int) -> None:
    """
    Load one monitor from PostgreSQL and execute it automatically.

    A new database session is required because scheduler jobs run
    outside the normal FastAPI request lifecycle.
    """

    with SessionLocal() as db:
        monitor = db.get(MonitorModel, monitor_id)

        # The monitor may have been deleted or disabled
        # after the scheduler job was created.
        if monitor is None or not monitor.is_active:
            return

        execute_monitor(
            monitor=monitor,
            db=db,
        )


def configure_monitor_jobs() -> None:
    """
    Rebuild all scheduler jobs from the active monitors stored
    in PostgreSQL.
    """

    # Remove old jobs so that duplicate jobs are not created.
    scheduler.remove_all_jobs()

    with SessionLocal() as db:
        statement = (
            select(MonitorModel)
            .where(MonitorModel.is_active.is_(True))
            .order_by(MonitorModel.id)
        )

        active_monitors = list(db.scalars(statement).all())

        for monitor in active_monitors:
            scheduler.add_job(
                run_scheduled_monitor,
                trigger="interval",
                seconds=monitor.interval_seconds,
                args=[monitor.id],
                id=f"monitor-{monitor.id}",
                replace_existing=True,
                max_instances=1,
                coalesce=True,
            )


def start_scheduler() -> None:
    """
    Start APScheduler and load jobs for all active monitors.
    """

    if not scheduler.running:
        scheduler.start()

    configure_monitor_jobs()


def stop_scheduler() -> None:
    """
    Stop APScheduler when the FastAPI application shuts down.
    """

    if scheduler.running:
        scheduler.shutdown(wait=False)