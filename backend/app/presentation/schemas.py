from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class WeatherResponse(BaseModel):
    city: str
    temperature: float = Field(..., description="Current temperature in Celsius")
    description: str = Field(..., description="Short text describing the weather condition")
    icon: str = Field(..., description="URL of the condition icon")
    timestamp: datetime
    language: str = Field(..., description="ISO code of the localized description")


class WeatherEnvelope(BaseModel):
    data: WeatherResponse


class HealthResponse(BaseModel):
    status: str = "ok"


class ErrorDetails(BaseModel):
    code: str
    message: str


class ErrorEnvelope(BaseModel):
    error: ErrorDetails
