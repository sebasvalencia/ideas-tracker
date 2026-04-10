import logging

from prometheus_fastapi_instrumentator import Instrumentator

_log = logging.getLogger(__name__)
_metrics_initialized = False


def setup_metrics(app) -> None:  # noqa: ANN001
    global _metrics_initialized
    if _metrics_initialized:
        return
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")
    _metrics_initialized = True
    _log.info("Prometheus metrics exposed at /metrics")
