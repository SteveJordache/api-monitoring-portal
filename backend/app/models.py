# NEW: We need datetime values for the execution timestamp.
from datetime import datetime, timezone

# NEW:
# Boolean      -> stores success/failure
# DateTime     -> stores when the check was executed
# ForeignKey   -> links a result to a monitor
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
)

# NEW:
# relationship -> defines the ORM relationship between results and monitors
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MonitorModel(Base):
    __tablename__ = "monitors"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )

    method: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="GET",
    )

    expected_status: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=200,
    )

    # NEW:
    # One monitor can have multiple execution results.
    results: Mapped[list["MonitorResultModel"]] = relationship(
        back_populates="monitor",
        cascade="all, delete-orphan",
    )


# NEW: Entire model for storing execution history.
class MonitorResultModel(Base):
    __tablename__ = "monitor_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # NEW:
    # Foreign key that connects this result to one monitor.
    monitor_id: Mapped[int] = mapped_column(
        ForeignKey(
            "monitors.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # NEW:
    # True when actual_status matches expected_status.
    success: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    # NEW:
    # HTTP status returned by the monitored endpoint.
    actual_status: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # NEW:
    # HTTP status configured in the monitor.
    expected_status: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # NEW:
    # Duration of the HTTP request in milliseconds.
    response_time_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # NEW:
    # UTC timestamp automatically created for every execution.
    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # NEW:
    # Each result belongs to exactly one monitor.
    monitor: Mapped["MonitorModel"] = relationship(
        back_populates="results",
    )