import structlog
import logging
from pathlib import Path
from app.core.config import settings

# Ensure logs directory exists
Path(settings.log_file).parent.mkdir(parents=True, exist_ok=True)

# Configure structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(
        file=open(settings.log_file, "a")
    ),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()