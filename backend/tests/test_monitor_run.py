from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_run_existing_monitor_successfully(monkeypatch) -> None:
    monitor_data = {
        "name": "Example API",
        "url": "https://example.com/health",
        "method": "GET",
        "expected_status": 200,
    }

    create_response = client.post("/monitors", json=monitor_data)
    monitor_id = create_response.json()["id"]

    class FakeResponse:
        status_code = 200

    def fake_request(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr("app.main.httpx.request", fake_request)

    run_response = client.post(f"/monitors/{monitor_id}/run")

    assert run_response.status_code == 200

    result = run_response.json()

    assert result["monitor_id"] == monitor_id
    assert result["success"] is True
    assert result["actual_status"] == 200
    assert result["expected_status"] == 200
    assert result["response_time_ms"] >= 0


def test_run_unknown_monitor_returns_404() -> None:
    response = client.post("/monitors/999/run")

    assert response.status_code == 404
    assert response.json() == {"detail": "Monitor not found"}
