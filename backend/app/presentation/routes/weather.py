from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.application.services import WeatherService
from app.domain.models import WeatherSnapshot
from app.infrastructure.metrics import track_weather_request
from app.presentation.dependencies import get_weather_service
from app.presentation.schemas import ErrorEnvelope, WeatherEnvelope, WeatherResponse

router = APIRouter(prefix="/api", tags=["weather"])


@router.get(
    "/weather",
    response_model=WeatherEnvelope,
    responses={400: {"model": ErrorEnvelope}, 404: {"model": ErrorEnvelope}, 503: {"model": ErrorEnvelope}},
)
async def get_weather(
    city: str = Query(..., description="City name (supports city or 'city,country')"),
    lang: str = Query("en", description="Localization language (en or ru)"),
    service: WeatherService = Depends(get_weather_service),
) -> WeatherEnvelope:
    lang_code = lang.lower()
    with track_weather_request(lang_code):
        snapshot = await service.execute(city, lang_code)
    return WeatherEnvelope(data=_to_response(snapshot))


def _to_response(snapshot: WeatherSnapshot) -> WeatherResponse:
    return WeatherResponse(
        city=snapshot.city,
        temperature=snapshot.temperature_c,
        description=snapshot.condition,
        icon=snapshot.icon_url,
        timestamp=snapshot.timestamp,
        language=snapshot.language,
    )
