# Weather Platform

Production-ready weather stack: FastAPI (Clean Architecture + Prometheus), Nuxt 3 (TypeScript, i18n), Docker Compose, Prometheus/blackbox monitoring и Grafana-дэшборд.

---

## 📁 Структура

```bash
backend/     FastAPI + uv + pytest + Prometheus metrics
frontend/    Nuxt 3 + TypeScript + Vitest + i18n
monitoring/  Prometheus + blackbox-exporter конфиги
grafana/     Datasource provisioning + Weather Service Overview.json
```

---

## ⚙️ Локальная разработка

### Backend (FastAPI + uv)

```bash
cd backend
uv sync --extra dev                # создаёт .venv
cp .env.example .env               # пропишите WEATHER_APP_WEATHER_API_KEY
uv run uvicorn app.main:app --reload
```
Переменные WEATHER_APP:

- WEATHER_API_KEY — ключ WeatherAPI (обязателен вне тестов)
- WEATHER_API_BASE_URL — дефолт https://api.weatherapi.com/v1
- REQUEST_TIMEOUT_SECONDS — таймаут HTTP (сек)
- APP_ENV — development|production|test
- CORS_ALLOW_ORIGINS — CSV origin’ов (например, http://localhost:3000)

### Frontend (Nuxt 3)

```bash
cd frontend
npm install
npm run dev
```
UI двуязычный (RU/EN), переключатель (LanguageSwitcher) меняет параметр lang в запросах, так что WeatherAPI сразу присылает локализованное описание. Температура отображается строго в °C.

---

## 🐳 Docker / Production-like стек

```bash
cp .env.example .env # локальный запуск
cp .env.example .env.prod # для docker-compose.prod.yml
```

# Дев-стек с мониторингом
```docker
docker compose up --build
```
# Прод-стек
```docker
docker compose -f docker-compose.prod.yml up --build
```
Сервисы:

- Backend → http://localhost:8000 (API + /metrics)
- Frontend → http://localhost:3000
- Prometheus → http://localhost:9090
- Grafana → http://localhost:3001 (admin/admin)
- Blackbox-exporter → health-probes /health и /

Grafana провиженит datasource prometheus и подхватывает дашборд **Weather Service Overview** с панелями:

1. weather_requests_total — rate запросов по языку
2. weather_request_latency_seconds — p90 латентность
3. weather_provider_errors_total — счётчики ошибок провайдера

---

## 📈 Мониторинг

- FastAPI экспортирует /metrics: latency/статус на каждую выдачу погоды + счётчики ошибок WeatherAPI.
- Prometheus дополнительно использует blackbox для проверки доступности фронта/бэка.
- Grafana читает Prometheus и отображает сразу готовый дашборд (grafana/dashboards/weather-overview.json).

---

## ✅ Тесты

### Backend

```bash
cd backend
uv run pytest  # pytest.ini включает --cov app
```
Тесты покрывают домен, use-case, интеграцию WeatherAPI (respx), REST-роуты и /metrics.

### Frontend

```bash
cd frontend
npm install
npm run test:unit
```
Vitest тестирует WeatherCard (в т.ч. корректный символ °C). При необходимости можно добавить новые тесты для composables/страниц.

---

## 🧱 Архитектурные заметки

- **Clean Architecture**: domain (WeatherSnapshot/interfaces) → application (WeatherService) → infrastructure (WeatherAPI + конфиг + метрики) → presentation (FastAPI-роуты/ошибки).
- **Локализация**: lang валидируется (en|ru) и уходит в WeatherAPI; фронт использует useWeatherI18n + словари src/i18n/messages.ts.
- **Monitoring-first**: Prometheus-инструментация (weather_requests_total, weather_request_latency_seconds, weather_provider_errors_total) + blackbox health-checks + Grafana dashboard.
- **Docker**: многостадийные build'ы (backend через uv-lock, frontend через Nuxt build); compose-файлы для dev/prod, единая сеть для сервисов.

---

## 🚀 Что планируется дальше

1. Добавить кэш/квотирование (Redis) для снижения нагрузки на WeatherAPI.
2. Auto-detect языка по заголовкам браузера.
3. Alertmanager/Slack-нотификации на базе текущих метрик.

---
