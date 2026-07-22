import pytest
from sqlalchemy import text

from app.database import engine


@pytest.fixture(autouse=True)
def clear_database_tables() -> None:
    # Clean both related tables and reset their ID sequences
    # before every test.
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                TRUNCATE TABLE
                    monitor_results,
                    monitors
                RESTART IDENTITY
                CASCADE
                """
            )
        )