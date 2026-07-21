from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

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
