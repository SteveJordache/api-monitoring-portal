from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_dashboard_summary_returns_expected_fields() -> None:
    response = client.get("/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "up" in data
    assert "down" in data
    assert "inactive" in data
    assert "not_checked" in data

    assert data["total"] == (
        data["up"]
        + data["down"]
        + data["inactive"]
        + data["not_checked"]
    )
