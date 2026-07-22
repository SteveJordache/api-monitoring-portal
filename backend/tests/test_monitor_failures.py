import httpx
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_timeout_is_stored_as_failed_result(monkeypatch) -> None:
    monitor_data = {
        "name": "Timeout API",
        "url": "https://example.com/slow",
        "method": "GET",
        "expected_status": 200,
    }

    create_response = client.post("/monitors", json=monitor_data)
    monitor_id = create_response.json()["id"]

    def fake_request(*args, **kwargs):
        raise httpx.TimeoutException("Test timeout")

    monkeypatch.setattr("app.services.httpx.request", fake_request)

    run_response = client.post(f"/monitors/{monitor_id}/run")

    assert run_response.status_code == 200

    result = run_response.json()

    assert result["monitor_id"] == monitor_id
    assert result["success"] is False
    assert result["actual_status"] is None
    assert result["expected_status"] == 200
    assert result["response_time_ms"] >= 0
    assert result["error_message"] == "Request timed out"

    history_response = client.get(
        f"/monitors/{monitor_id}/results"
    )

    assert history_response.status_code == 200

    history = history_response.json()

    assert len(history) == 1
    assert history[0]["success"] is False
    assert history[0]["actual_status"] is None
    assert history[0]["error_message"] == "Request timed out"


def test_connection_error_is_stored_as_failed_result(monkeypatch) -> None:
    monitor_data = {
        "name": "Unavailable API",
        "url": "https://unavailable.example.com",
        "method": "GET",
        "expected_status": 200,
    }

    create_response = client.post("/monitors", json=monitor_data)
    monitor_id = create_response.json()["id"]

    request = httpx.Request(
        method="GET",
        url="https://unavailable.example.com",
    )

    def fake_request(*args, **kwargs):
        raise httpx.ConnectError(
            "Connection refused",
            request=request,
        )

    monkeypatch.setattr("app.services.httpx.request", fake_request)

    run_response = client.post(f"/monitors/{monitor_id}/run")

    assert run_response.status_code == 200

    result = run_response.json()

    assert result["monitor_id"] == monitor_id
    assert result["success"] is False
    assert result["actual_status"] is None
    assert result["expected_status"] == 200
    assert result["response_time_ms"] >= 0
    assert result["error_message"].startswith("Request failed:")
    assert "Connection refused" in result["error_message"]

    history_response = client.get(
        f"/monitors/{monitor_id}/results"
    )

    assert history_response.status_code == 200

    history = history_response.json()

    assert len(history) == 1
    assert history[0]["success"] is False
    assert history[0]["actual_status"] is None
    assert "Connection refused" in history[0]["error_message"]