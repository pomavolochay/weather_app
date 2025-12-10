from __future__ import annotations

import time
from contextlib import contextmanager

from prometheus_client import Counter, Histogram

WEATHER_REQUESTS_TOTAL = Counter(
    "weather_requests_total",
    "Total number of weather lookups served by status.",
    labelnames=("status", "lang"),
)

WEATHER_REQUEST_LATENCY_SECONDS = Histogram(
    "weather_request_latency_seconds",
    "Latency of weather lookups (seconds).",
    labelnames=("status", "lang"),
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2, 3, 5),
)

WEATHER_PROVIDER_ERRORS_TOTAL = Counter(
    "weather_provider_errors_total",
    "Count of upstream provider errors by code.",
    labelnames=("code",),
)


@contextmanager
def track_weather_request(lang: str):
    start = time.perf_counter()
    status = "success"
    try:
        yield
    except Exception as exc:
        status = getattr(exc, "code", "error")
        raise
    finally:
        duration = time.perf_counter() - start
        WEATHER_REQUESTS_TOTAL.labels(status=status, lang=lang).inc()
        WEATHER_REQUEST_LATENCY_SECONDS.labels(status=status, lang=lang).observe(duration)


def record_provider_error(code: str) -> None:
    WEATHER_PROVIDER_ERRORS_TOTAL.labels(code=code).inc()
