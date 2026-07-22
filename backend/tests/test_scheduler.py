from app.database import SessionLocal
from app.models import MonitorModel
from app.scheduler import run_scheduled_monitor


def create_test_monitor(
    *,
    name: str,
    is_active: bool,
) -> int:
    """
    Create a monitor directly in the test database
    and return its generated ID.
    """

    with SessionLocal() as db:
        monitor = MonitorModel(
            name=name,
            url="https://example.com/",
            method="GET",
            expected_status=200,
            interval_seconds=10,
            is_active=is_active,
        )

        db.add(monitor)
        db.commit()
        db.refresh(monitor)

        return monitor.id


def test_scheduler_executes_active_monitor(monkeypatch) -> None:
    monitor_id = create_test_monitor(
        name="Active Monitor",
        is_active=True,
    )

    executed_monitor_ids: list[int] = []

    def fake_execute_monitor(*, monitor, db):
        executed_monitor_ids.append(monitor.id)

    monkeypatch.setattr(
        "app.scheduler.execute_monitor",
        fake_execute_monitor,
    )

    run_scheduled_monitor(monitor_id)

    assert executed_monitor_ids == [monitor_id]


def test_scheduler_skips_inactive_monitor(monkeypatch) -> None:
    monitor_id = create_test_monitor(
        name="Inactive Monitor",
        is_active=False,
    )

    executed_monitor_ids: list[int] = []

    def fake_execute_monitor(*, monitor, db):
        executed_monitor_ids.append(monitor.id)

    monkeypatch.setattr(
        "app.scheduler.execute_monitor",
        fake_execute_monitor,
    )

    run_scheduled_monitor(monitor_id)

    assert executed_monitor_ids == []