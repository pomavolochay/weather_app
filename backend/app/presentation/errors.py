from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from app.domain.exceptions import WeatherError
from app.presentation.schemas import ErrorDetails, ErrorEnvelope


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(WeatherError)
    async def handle_weather_error(request: Request, exc: WeatherError) -> JSONResponse:
        status_code = _status_from_code(exc.code)
        return _error_response(code=exc.code, message=str(exc), status_code=status_code)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        return _error_response(
            code="validation_error",
            message="; ".join(err["msg"] for err in exc.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
        return _error_response(
            code="http_error",
            message=exc.detail if isinstance(exc.detail, str) else "HTTP error",
            status_code=exc.status_code,
        )


def _status_from_code(code: str) -> int:
    mapping = {
        "city_not_found": status.HTTP_404_NOT_FOUND,
        "rate_limited": status.HTTP_429_TOO_MANY_REQUESTS,
        "provider_unavailable": status.HTTP_503_SERVICE_UNAVAILABLE,
        "invalid_city": status.HTTP_400_BAD_REQUEST,
    }
    return mapping.get(code, status.HTTP_400_BAD_REQUEST)


def _error_response(*, code: str, message: str, status_code: int) -> JSONResponse:
    payload = ErrorEnvelope(error=ErrorDetails(code=code, message=message))
    return JSONResponse(status_code=status_code, content=payload.model_dump())
