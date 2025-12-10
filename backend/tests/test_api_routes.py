from __future__ import annotations


def test_get_weather_returns_payload(api_client):
    response = api_client.get("/api/weather", params={"city": "Berlin"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["city"] == "Berlin"
    assert "temperature" in payload["data"]
    assert "description" in payload["data"]
    assert payload["data"]["language"] == "en"


def test_get_weather_requires_city(api_client):
    response = api_client.get("/api/weather")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_get_weather_supports_localization(api_client):
    response = api_client.get("/api/weather", params={"city": "Rome", "lang": "ru"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["language"] == "ru"
