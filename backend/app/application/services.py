from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone

from app.domain.exceptions import WeatherError
from app.domain.interfaces import WeatherProvider
from app.domain.models import WeatherSnapshot

SUPPORTED_LANGS = {"en", "ru"}


class WeatherService:
    """Use case responsible for retrieving current weather snapshots."""

    def __init__(self, provider: WeatherProvider):
        self._provider = provider

    async def execute(self, city: str, lang: str = "en") -> WeatherSnapshot:
        city_name = self._normalize_city(city)
        lang_code = self._normalize_lang(lang)
        snapshot = await self._provider.get_current_weather(city_name, lang_code)
        snapshot = self._ensure_timezone(snapshot)
        if snapshot.language != lang_code:
            snapshot = replace(snapshot, language=lang_code)
        return snapshot

    @staticmethod
    def _normalize_city(city: str) -> str:
        if not city or not city.strip():
            raise WeatherError("City name must be provided", code="invalid_city")
        normalized = " ".join(part for part in city.split())
        return normalized

    @staticmethod
    def _normalize_lang(lang: str) -> str:
        if not lang:
            return "en"
        normalized = lang.lower()
        if normalized not in SUPPORTED_LANGS:
            raise WeatherError(f"Unsupported language '{lang}'", code="invalid_language")
        return normalized

    @staticmethod
    def _ensure_timezone(snapshot: WeatherSnapshot) -> WeatherSnapshot:
        if snapshot.timestamp.tzinfo is None:
            timestamp = snapshot.timestamp.replace(tzinfo=timezone.utc)
            return WeatherSnapshot(
                city=snapshot.city,
                temperature_c=snapshot.temperature_c,
                condition=snapshot.condition,
                icon_url=snapshot.icon_url,
                timestamp=timestamp,
                language=snapshot.language,
            )
        return snapshot
