from __future__ import annotations

from typing import Optional

from app.application.services import WeatherService
from app.infrastructure.container import ServiceContainer

_container: Optional[ServiceContainer] = None


def set_container(container: ServiceContainer) -> None:
    global _container
    _container = container


def clear_container() -> None:
    global _container
    _container = None


def get_weather_service() -> WeatherService:
    if _container is None:
        raise RuntimeError("Container is not configured")
    return _container.weather_service
