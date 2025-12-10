from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="WEATHER_APP_", env_file=".env", case_sensitive=False, populate_by_name=True
    )

    weather_api_key: str = "demo-key"
    weather_api_base_url: AnyHttpUrl = "https://api.weatherapi.com/v1"
    request_timeout_seconds: float = 10.0
    app_env: Literal["development", "production", "test"] = "development"
    cors_allow_origins_raw: str = Field(default="*", alias="cors_allow_origins")

    @property
    def cors_allow_origins(self) -> list[str]:
        value = (self.cors_allow_origins_raw or "").strip()
        if not value or value == "*":
            return ["*"]
        return [origin.strip() for origin in value.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
