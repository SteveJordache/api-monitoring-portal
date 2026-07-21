from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_and_list_monitor() -> None:
    monitor_data = {
        "name": "Example API",
        "url": "https://example.com/health",
        "method": "GET",
        "expected_status": 200,
    }

    create_response = client.post("/monitors", json=monitor_data)

    assert create_response.status_code == 201

    created_monitor = create_response.json()

    assert created_monitor["id"] > 0
    assert created_monitor["name"] == "Example API"
    assert created_monitor["url"] == "https://example.com/health"
    assert created_monitor["method"] == "GET"
    assert created_monitor["expected_status"] == 200

    list_response = client.get("/monitors")

    assert list_response.status_code == 200
    assert list_response.json() == [created_monitor]