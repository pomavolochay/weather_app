from __future__ import annotations


class WeatherError(Exception):
    """Base exception for domain-level weather errors."""

    def __init__(self, message: str, *, code: str = "weather_error"):
        super().__init__(message)
        self.code = code


class CityNotFoundError(WeatherError):
    def __init__(self, city: str):
        super().__init__(f"City '{city}' was not found", code="city_not_found")
        self.city = city


class ProviderRateLimitError(WeatherError):
    def __init__(self):
        super().__init__("Weather provider rate limit exceeded", code="rate_limited")


class ProviderUnavailableError(WeatherError):
    def __init__(self, details: str | None = None):
        message = "Weather provider is temporarily unavailable"
        if details:
            message = f"{message}: {details}"
        super().__init__(message, code="provider_unavailable")
        self.details = details
