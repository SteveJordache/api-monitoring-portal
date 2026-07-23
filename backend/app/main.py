from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import MonitorModel, MonitorResultModel
from app.scheduler import (
    configure_monitor_jobs,
    start_scheduler,
    stop_scheduler,
)
from app.services import execute_monitor


# Create database tables if they do not already exist.
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Start the scheduler when FastAPI starts and stop it
    when FastAPI shuts down.
    """
    start_scheduler()

    try:
        yield
    finally:
        stop_scheduler()


app = FastAPI(
    title="API Monitoring Portal",
    version="0.1.0",
    lifespan=lifespan,
)


# Serve CSS and JavaScript files.
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)


# Configure HTML templates.
templates = Jinja2Templates(
    directory="app/templates",
)


DatabaseSession = Annotated[Session, Depends(get_db)]


class MonitorCreate(BaseModel):
    name: str
    url: HttpUrl
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = "GET"
    expected_status: int = 200
    interval_seconds: int = Field(default=60, ge=10)
    is_active: bool = True


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

class DashboardSummary(BaseModel):
    total: int
    up: int
    down: int
    inactive: int
    not_checked: int


@app.get(
    "/",
    response_class=HTMLResponse,
)
def home(request: Request):
    """
    Render the main web interface.
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


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
        interval_seconds=monitor_data.interval_seconds,
        is_active=monitor_data.is_active,
    )

    db.add(monitor)
    db.commit()
    db.refresh(monitor)

    configure_monitor_jobs()

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

    result = execute_monitor(
        monitor=monitor,
        db=db,
    )

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

@app.get(
    "/dashboard/summary",
    response_model=DashboardSummary,
)
def get_dashboard_summary(
    db: DatabaseSession,
) -> DashboardSummary:
    monitors = list(
        db.scalars(
            select(MonitorModel).order_by(MonitorModel.id)
        ).all()
    )

    up = 0
    down = 0
    inactive = 0
    not_checked = 0

    for monitor in monitors:
        if not monitor.is_active:
            inactive += 1
            continue

        latest_result_statement = (
            select(MonitorResultModel)
            .where(MonitorResultModel.monitor_id == monitor.id)
            .order_by(MonitorResultModel.checked_at.desc())
            .limit(1)
        )

        latest_result = db.scalar(latest_result_statement)

        if latest_result is None:
            not_checked += 1
        elif latest_result.success:
            up += 1
        else:
            down += 1

    return DashboardSummary(
        total=len(monitors),
        up=up,
        down=down,
        inactive=inactive,
        not_checked=not_checked,
    )