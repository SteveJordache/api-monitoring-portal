from time import perf_counter
from typing import Annotated, Literal

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, HttpUrl
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import MonitorModel


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API Monitoring Portal",
    version="0.1.0",
)


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
    actual_status: int
    expected_status: int
    response_time_ms: int


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


@app.get("/monitors", response_model=list[Monitor])
def list_monitors(db: DatabaseSession) -> list[MonitorModel]:
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

    response = httpx.request(
        method=monitor.method,
        url=monitor.url,
        timeout=10.0,
    )

    response_time_ms = int((perf_counter() - start_time) * 1000)

    return MonitorRunResult(
        monitor_id=monitor.id,
        success=response.status_code == monitor.expected_status,
        actual_status=response.status_code,
        expected_status=monitor.expected_status,
        response_time_ms=response_time_ms,
    )
