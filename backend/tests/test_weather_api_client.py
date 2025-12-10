from __future__ import annotations

from datetime import datetime, timezone

import pytest
import respx
from httpx import Response

from app.domain.exceptions import CityNotFoundError, ProviderRateLimitError
from app.infrastructure.config import Settings
from app.infrastructure.weather_api_client import WeatherAPIClient


def _payload() -> dict:
    return {
        "location": {"name": "Paris"},
        "current": {
            "temp_c": 13.4,
            "condition": {"text": "Cloudy", "icon": "//cdn.weatherapi.com/icon.png"},
            "last_updated_epoch": int(datetime(2023, 1, 1, 11, 0, tzinfo=timezone.utc).timestamp()),
        },
    }


@pytest.mark.asyncio
async def test_weather_api_client_maps_payload(monkeypatch):
    settings = Settings(weather_api_key="abc", weather_api_base_url="https://example.com")
    client = WeatherAPIClient(settings)
    await client.start()
    with respx.mock(base_url="https://example.com") as mock:
        mock.get("/current.json").respond(200, json=_payload())
        snapshot = await client.get_current_weather("Paris", "ru")
        assert snapshot.city == "Paris"
        assert snapshot.temperature_c == 13.4
        assert snapshot.icon_url.startswith("https://")
        assert snapshot.language == "ru"
    await client.close()


@pytest.mark.asyncio
async def test_weather_api_client_handles_not_found():
    settings = Settings(weather_api_key="abc", weather_api_base_url="https://example.com")
    client = WeatherAPIClient(settings)
    await client.start()
    with respx.mock(base_url="https://example.com") as mock:
        mock.get("/current.json").respond(400, json={"error": {"message": "No matching location found"}})
        with pytest.raises(CityNotFoundError):
            await client.get_current_weather("Atlantis", "en")
    await client.close()


@pytest.mark.asyncio
async def test_weather_api_client_handles_rate_limit():
    settings = Settings(weather_api_key="abc", weather_api_base_url="https://example.com")
    client = WeatherAPIClient(settings)
    await client.start()
    with respx.mock(base_url="https://example.com") as mock:
        mock.get("/current.json").respond(429, json={"error": {"message": "Rate limit"}})
        with pytest.raises(ProviderRateLimitError):
            await client.get_current_weather("Paris", "en")
    await client.close()
