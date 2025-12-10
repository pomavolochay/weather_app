from __future__ import annotations

from dataclasses import dataclass

from app.application.services import WeatherService
from app.infrastructure.config import Settings, get_settings
from app.infrastructure.weather_api_client import WeatherAPIClient


@dataclass(slots=True)
class ServiceContainer:
    """Lightweight container wiring infrastructure to application services."""

    settings: Settings
    weather_provider: WeatherAPIClient
    weather_service: WeatherService

    @classmethod
    def build(cls, settings: Settings | None = None) -> "ServiceContainer":
        app_settings = settings or get_settings()
        provider = WeatherAPIClient(app_settings)
        service = WeatherService(provider)
        return cls(settings=app_settings, weather_provider=provider, weather_service=service)
