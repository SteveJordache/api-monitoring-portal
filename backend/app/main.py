from typing import Literal

from fastapi import FastAPI, status
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
