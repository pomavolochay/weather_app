from __future__ import annotations

from contextlib import asynccontextmanager
from inspect import iscoroutinefunction

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.container import ServiceContainer
from app.presentation import dependencies
from app.presentation.errors import register_error_handlers
from app.presentation.routes import health, metrics, weather


def create_app(container: ServiceContainer | None = None) -> FastAPI:
    service_container = container or ServiceContainer.build()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        dependencies.set_container(service_container)
        await _call_optional(service_container.weather_provider, "start")
        try:
            yield
        finally:
            await _call_optional(service_container.weather_provider, "close")
            dependencies.clear_container()

    settings = service_container.settings

    app = FastAPI(title="Weather Service", version="1.0.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_error_handlers(app)
    app.include_router(health.router)
    app.include_router(weather.router)
    app.include_router(metrics.router)
    return app


app = create_app()


async def _call_optional(obj: object, method: str) -> None:
    attribute = getattr(obj, method, None)
    if attribute is None:
        return
    if iscoroutinefunction(attribute):
        await attribute()
        return
    result = attribute()
    if hasattr(result, "__await__"):
        await result  # pragma: no cover
