import pytest
from sqlalchemy import text

from app.database import engine


@pytest.fixture(autouse=True)
def clear_monitors_table() -> None:
    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE monitors RESTART IDENTITY")
        )
