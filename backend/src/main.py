import logging

from fastapi import FastAPI, Request
from slowapi.middleware import SlowAPIMiddleware

from src.app.adapters.inbound.rest.rate_limiter import limiter
from src.app.adapters.inbound.rest.routers.auth_router import router as auth_router
from src.app.adapters.inbound.rest.routers.ideas_router import router as ideas_router
from src.app.adapters.inbound.rest.routers.logs_router import router as logs_router
from src.app.adapters.inbound.rest.routers.ratings_router import router as ratings_router
from src.app.adapters.outbound.observability.logging_config import setup_logging
from src.app.adapters.outbound.observability.metrics import setup_metrics
from src.app.adapters.outbound.observability.tracing import current_trace_id, setup_tracing
from src.app.adapters.outbound.persistence.sqlalchemy.session import engine
from src.app.bootstrap.settings import settings

app = FastAPI(title="Ideas Tracker API")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
setup_logging()
_log = logging.getLogger(__name__)

if settings.OTEL_ENABLED:
    setup_tracing(
        app=app,
        engine=engine,
        service_name=settings.OTEL_SERVICE_NAME,
        otlp_endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT,
    )
if settings.METRICS_ENABLED:
    setup_metrics(app)


app.include_router(ideas_router)
app.include_router(logs_router)
app.include_router(ratings_router)
app.include_router(auth_router)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    trace_id = current_trace_id()
    if trace_id:
        response.headers["X-Trace-Id"] = trace_id
    return response

@app.get("/health")
def health() -> dict[str, str]:
    _log.info("Health endpoint called")
    return {"status": "ok"}