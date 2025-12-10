from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from app.application.services import WeatherService
from app.domain.interfaces import WeatherProvider
from app.domain.models import WeatherSnapshot
from app.infrastructure.config import Settings
from app.infrastructure.container import ServiceContainer
from app.presentation.api import create_app


class StubWeatherProvider(WeatherProvider):
    def __init__(self, snapshot: WeatherSnapshot):
        self.snapshot = snapshot
        self.requested: list[tuple[str, str]] = []

    async def get_current_weather(self, city: str, lang: str) -> WeatherSnapshot:
        self.requested.append((city, lang))
        return WeatherSnapshot(
            city=city,
            temperature_c=self.snapshot.temperature_c,
            condition=self.snapshot.condition,
            icon_url=self.snapshot.icon_url,
            timestamp=self.snapshot.timestamp,
            language=lang,
        )

    async def start(self) -> None:  # pragma: no cover - trivial for tests
        return None

    async def close(self) -> None:  # pragma: no cover - trivial for tests
        return None


@pytest.fixture
def sample_snapshot() -> WeatherSnapshot:
    return WeatherSnapshot(
        city="Rome",
        temperature_c=23.5,
        condition="Sunny",
        icon_url="https://cdn.weather/icon.png",
        timestamp=datetime(2023, 9, 29, 12, 0, tzinfo=timezone.utc),
        language="en",
    )


@pytest.fixture
def api_client(sample_snapshot: WeatherSnapshot) -> Generator[TestClient, None, None]:
    provider = StubWeatherProvider(sample_snapshot)
    service = WeatherService(provider)
    container = ServiceContainer(settings=Settings(weather_api_key="test", app_env="test"), weather_provider=provider, weather_service=service)
    app = create_app(container)
    with TestClient(app) as client:
        yield client
