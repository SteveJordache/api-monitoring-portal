from time import perf_counter

import httpx
from sqlalchemy.orm import Session

from app.models import MonitorModel, MonitorResultModel


def execute_monitor(
    monitor: MonitorModel,
    db: Session,
) -> MonitorResultModel:
    """
    Execute one monitor, persist the result and return it.
    """

    start_time = perf_counter()

    actual_status: int | None = None
    error_message: str | None = None
    success = False

    try:
        response = httpx.request(
            method=monitor.method,
            url=monitor.url,
            timeout=10.0,
        )

        actual_status = response.status_code
        success = actual_status == monitor.expected_status

    except httpx.TimeoutException:
        error_message = "Request timed out"

    except httpx.RequestError as exc:
        error_message = f"Request failed: {exc}"

    response_time_ms = int((perf_counter() - start_time) * 1000)

    result = MonitorResultModel(
        monitor_id=monitor.id,
        success=success,
        actual_status=actual_status,
        expected_status=monitor.expected_status,
        response_time_ms=response_time_ms,
        error_message=error_message,
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return result