from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class WeatherSnapshot:
    """Domain entity describing a normalized weather reading."""

    city: str
    temperature_c: float
    condition: str
    icon_url: str
    timestamp: datetime
    language: str = "en"
