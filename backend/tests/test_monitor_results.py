from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_run_monitor_stores_result_and_returns_history(monkeypatch) -> None:
    monitor_data = {
        "name": "History API",
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

    history_response = client.get(
        f"/monitors/{monitor_id}/results"
    )

    assert history_response.status_code == 200

    results = history_response.json()

    assert len(results) == 1
    assert results[0]["monitor_id"] == monitor_id
    assert results[0]["success"] is True
    assert results[0]["actual_status"] == 200
    assert results[0]["expected_status"] == 200
    assert results[0]["response_time_ms"] >= 0
    assert results[0]["checked_at"] is not None


def test_results_for_unknown_monitor_returns_404() -> None:
    response = client.get("/monitors/999/results")

    assert response.status_code == 404
    assert response.json() == {"detail": "Monitor not found"}