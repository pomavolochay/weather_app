from __future__ import annotations


def test_metrics_endpoint_exposes_prometheus(api_client):
    response = api_client.get("/metrics")
    assert response.status_code == 200
    assert "weather_requests_total" in response.text
