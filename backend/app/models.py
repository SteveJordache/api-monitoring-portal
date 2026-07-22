from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
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

    # One monitor can have multiple execution results.
    results: Mapped[list["MonitorResultModel"]] = relationship(
        back_populates="monitor",
        cascade="all, delete-orphan",
    )


class MonitorResultModel(Base):
    __tablename__ = "monitor_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Links this execution result to one monitor.
    monitor_id: Mapped[int] = mapped_column(
        ForeignKey(
            "monitors.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # True when the monitor execution matched the expected result.
    success: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    # UPDATED:
    # A network failure has no HTTP status, so this field must allow NULL.
    actual_status: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    expected_status: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    response_time_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # NEW:
    # Stores timeout, DNS, connection, SSL or other request errors.
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Each result belongs to exactly one monitor.
    monitor: Mapped["MonitorModel"] = relationship(
        back_populates="results",
    )