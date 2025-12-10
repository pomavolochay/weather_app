from __future__ import annotations

import httpx
from datetime import datetime, timezone
from typing import Any

from app.domain.exceptions import (
    CityNotFoundError,
    ProviderRateLimitError,
    ProviderUnavailableError,
)
from app.domain.interfaces import WeatherProvider
from app.domain.models import WeatherSnapshot
from app.infrastructure.config import Settings
from app.infrastructure.metrics import record_provider_error


class WeatherAPIClient(WeatherProvider):
    """Adapter responsible for talking to WeatherAPI."""

    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None):
        self._settings = settings
        self._client = client
        self._owns_client = client is None

    async def start(self) -> None:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=str(self._settings.weather_api_base_url),
                timeout=self._settings.request_timeout_seconds,
            )

    async def close(self) -> None:
        if self._owns_client and self._client:
            await self._client.aclose()
            self._client = None

    async def get_current_weather(self, city: str, lang: str) -> WeatherSnapshot:
        if self._client is None:
            await self.start()

        assert self._client is not None
        params = {"key": self._settings.weather_api_key, "q": city, "aqi": "no", "lang": lang}
        try:
            response = await self._client.get("/current.json", params=params)
        except httpx.HTTPError as exc:
            raise ProviderUnavailableError(str(exc)) from exc

        if response.status_code == 400 and _contains_message(response, "No matching location found"):
            record_provider_error("city_not_found")
            raise CityNotFoundError(city)
        if response.status_code == 429:
            record_provider_error("rate_limited")
            raise ProviderRateLimitError()
        if response.status_code >= 500:
            record_provider_error("provider_unavailable")
            raise ProviderUnavailableError(f"Status {response.status_code}")
        if response.status_code >= 400:
            record_provider_error("provider_error")
            raise ProviderUnavailableError(f"Unexpected status {response.status_code}")

        payload = response.json()
        return self._map_payload(payload, lang)

    @staticmethod
    def _map_payload(payload: dict[str, Any], lang: str) -> WeatherSnapshot:
        location = payload.get("location", {})
        current = payload.get("current", {})
        condition = current.get("condition", {})
        timestamp = WeatherAPIClient._parse_timestamp(current)
        icon = WeatherAPIClient._normalize_icon(condition.get("icon", ""))
        return WeatherSnapshot(
            city=location.get("name") or location.get("region") or "Unknown",
            temperature_c=float(current.get("temp_c")),
            condition=condition.get("text") or "Unknown",
            icon_url=icon,
            timestamp=timestamp,
            language=lang,
        )

    @staticmethod
    def _parse_timestamp(current: dict[str, Any]) -> datetime:
        epoch = current.get("last_updated_epoch")
        if epoch is not None:
            return datetime.fromtimestamp(int(epoch), tz=timezone.utc)
        last_updated = current.get("last_updated")
        if last_updated:
            return datetime.fromisoformat(last_updated)
        return datetime.now(tz=timezone.utc)

    @staticmethod
    def _normalize_icon(icon: str) -> str:
        if not icon:
            return ""
        if icon.startswith("//"):
            return f"https:{icon}"
        return icon


def _contains_message(response: httpx.Response, expected: str) -> bool:
    try:
        data = response.json()
    except ValueError:
        return expected in response.text
    error = data.get("error") if isinstance(data, dict) else None
    message = ""
    if isinstance(error, dict):
        message = error.get("message", "")
    return expected.lower() in message.lower()
