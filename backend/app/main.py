from time import perf_counter
from typing import Literal

import httpx
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, HttpUrl


app = FastAPI(
    title="API Monitoring Portal",
    version="0.1.0",
)


class MonitorCreate(BaseModel):
    name: str
    url: HttpUrl
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = "GET"
    expected_status: int = 200


class Monitor(MonitorCreate):
    id: int


class MonitorRunResult(BaseModel):
    monitor_id: int
    success: bool
    actual_status: int
    expected_status: int
    response_time_ms: int


monitors: list[Monitor] = []


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
def create_monitor(monitor_data: MonitorCreate) -> Monitor:
    monitor = Monitor(
        id=len(monitors) + 1,
        **monitor_data.model_dump(),
    )

    monitors.append(monitor)

    return monitor


@app.get("/monitors", response_model=list[Monitor])
def list_monitors() -> list[Monitor]:
    return monitors


@app.post(
    "/monitors/{monitor_id}/run",
    response_model=MonitorRunResult,
)
def run_monitor(monitor_id: int) -> MonitorRunResult:
    monitor = next(
        (item for item in monitors if item.id == monitor_id),
        None,
    )

    if monitor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found",
        )

    start_time = perf_counter()

    response = httpx.request(
        method=monitor.method,
        url=str(monitor.url),
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
