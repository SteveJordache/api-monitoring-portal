from datetime import datetime
from time import perf_counter
from typing import Annotated, Literal

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, HttpUrl
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import MonitorModel, MonitorResultModel


# Create database tables if they do not already exist.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API Monitoring Portal",
    version="0.1.0",
)


# FastAPI dependency type for database sessions.
DatabaseSession = Annotated[Session, Depends(get_db)]


class MonitorCreate(BaseModel):
    name: str
    url: HttpUrl
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = "GET"
    expected_status: int = 200


class Monitor(MonitorCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class MonitorRunResult(BaseModel):
    monitor_id: int
    success: bool
    actual_status: int | None
    expected_status: int
    response_time_ms: int
    error_message: str | None


class MonitorResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    monitor_id: int
    success: bool
    actual_status: int | None
    expected_status: int
    response_time_ms: int
    error_message: str | None
    checked_at: datetime


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "api-monitoring-backend",
    }


@app.post(
    "/monitors",
    response_model=Monitor,
    status_code=status.HTTP_201_CREATED,
)
def create_monitor(
    monitor_data: MonitorCreate,
    db: DatabaseSession,
) -> MonitorModel:
    monitor = MonitorModel(
        name=monitor_data.name,
        url=str(monitor_data.url),
        method=monitor_data.method,
        expected_status=monitor_data.expected_status,
    )

    db.add(monitor)
    db.commit()
    db.refresh(monitor)

    return monitor


@app.get(
    "/monitors",
    response_model=list[Monitor],
)
def list_monitors(
    db: DatabaseSession,
) -> list[MonitorModel]:
    statement = select(MonitorModel).order_by(MonitorModel.id)

    return list(db.scalars(statement).all())


@app.post(
    "/monitors/{monitor_id}/run",
    response_model=MonitorRunResult,
)
def run_monitor(
    monitor_id: int,
    db: DatabaseSession,
) -> MonitorRunResult:
    monitor = db.get(MonitorModel, monitor_id)

    if monitor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found",
        )

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

    # Persist both successful and failed executions.
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

    return MonitorRunResult(
        monitor_id=result.monitor_id,
        success=result.success,
        actual_status=result.actual_status,
        expected_status=result.expected_status,
        response_time_ms=result.response_time_ms,
        error_message=result.error_message,
    )


@app.get(
    "/monitors/{monitor_id}/results",
    response_model=list[MonitorResult],
)
def list_monitor_results(
    monitor_id: int,
    db: DatabaseSession,
) -> list[MonitorResultModel]:
    monitor = db.get(MonitorModel, monitor_id)

    if monitor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found",
        )

    statement = (
        select(MonitorResultModel)
        .where(MonitorResultModel.monitor_id == monitor_id)
        .order_by(MonitorResultModel.checked_at.desc())
    )

    return list(db.scalars(statement).all())