from __future__ import annotations

from abc import ABC, abstractmethod

from .models import WeatherSnapshot


class WeatherProvider(ABC):
    """Abstraction for a weather provider adapter."""

    @abstractmethod
    async def get_current_weather(self, city: str, lang: str) -> WeatherSnapshot:
        """Return a normalized snapshot for the requested city."""
