from __future__ import annotations

from dataclasses import replace
from datetime import datetime

import pytest

from app.application.services import WeatherService
from app.domain.exceptions import WeatherError
from app.domain.interfaces import WeatherProvider
from app.domain.models import WeatherSnapshot


class DummyProvider(WeatherProvider):
    def __init__(self, snapshot: WeatherSnapshot):
        self.snapshot = snapshot
        self.calls: list[tuple[str, str]] = []

    async def get_current_weather(self, city: str, lang: str) -> WeatherSnapshot:
        self.calls.append((city, lang))
        return replace(self.snapshot, city=city, language=lang)


@pytest.mark.asyncio
async def test_service_normalizes_input(sample_snapshot: WeatherSnapshot):
    service = WeatherService(DummyProvider(sample_snapshot))
    result = await service.execute("  London ", "ru")
    assert result.city == "London"
    assert result.language == "ru"


@pytest.mark.asyncio
async def test_service_rejects_empty_city(sample_snapshot: WeatherSnapshot):
    service = WeatherService(DummyProvider(sample_snapshot))
    with pytest.raises(WeatherError):
        await service.execute("   ")


@pytest.mark.asyncio
async def test_service_rejects_invalid_language(sample_snapshot: WeatherSnapshot):
    service = WeatherService(DummyProvider(sample_snapshot))
    with pytest.raises(WeatherError):
        await service.execute("Rome", "de")


@pytest.mark.asyncio
async def test_service_adds_timezone(sample_snapshot: WeatherSnapshot):
    naive_snapshot = replace(sample_snapshot, timestamp=datetime(2023, 1, 1, 12, 0))
    service = WeatherService(DummyProvider(naive_snapshot))
    result = await service.execute("Madrid")
    assert result.timestamp.tzinfo is not None
