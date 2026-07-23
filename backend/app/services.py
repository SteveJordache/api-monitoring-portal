from time import perf_counter

import httpx
from sqlalchemy.orm import Session

from app.metrics import (
    MONITOR_EXECUTION_DURATION_SECONDS,
    MONITOR_EXECUTION_FAILURES_TOTAL,
    MONITOR_EXECUTIONS_TOTAL,
)
from app.models import MonitorModel, MonitorResultModel


def execute_monitor(
    monitor: MonitorModel,
    db: Session,
) -> MonitorResultModel:
    """
    Execute one monitor, persist the result and update Prometheus metrics.
    """

    start_time = perf_counter()

    actual_status: int | None = None
    error_message: str | None = None
    error_type: str | None = None
    success = False

    try:
        response = httpx.request(
            method=monitor.method,
            url=monitor.url,
            timeout=10.0,
        )

        actual_status = response.status_code
        success = actual_status == monitor.expected_status

        if not success:
            error_type = "unexpected_status"

    except httpx.TimeoutException:
        error_message = "Request timed out"
        error_type = "timeout"

    except httpx.RequestError as exc:
        error_message = f"Request failed: {exc}"
        error_type = "request_error"

    response_time_seconds = perf_counter() - start_time
    response_time_ms = int(response_time_seconds * 1000)

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

    monitor_id_label = str(monitor.id)
    success_label = str(success).lower()

    MONITOR_EXECUTIONS_TOTAL.labels(
        monitor_id=monitor_id_label,
        success=success_label,
    ).inc()

    MONITOR_EXECUTION_DURATION_SECONDS.labels(
        monitor_id=monitor_id_label,
    ).observe(response_time_seconds)

    if error_type is not None:
        MONITOR_EXECUTION_FAILURES_TOTAL.labels(
            monitor_id=monitor_id_label,
            error_type=error_type,
        ).inc()

    return result
