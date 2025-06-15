import logging
import sys

import structlog
from structlog.types import Processor


def setup_logging():
    """
    Configure structured logging for the application.

    This setup uses structlog to process and format logs as JSON,
    """
    # Define the processor chain for structlog
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    # Configure the standard logging library to be a sink for structlog
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)

    # Configure structlog itself
    structlog.configure(
        processors=shared_processors
        + [
            # Prepare the log record for the standard library
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Use a JSON renderer for the final output
    # This is the key part for structured logging
    # Ascii false to allow unicode characters and emojis in logs
    renderer = structlog.processors.JSONRenderer(ensure_ascii=False)

    # Get the root loggers handler and set our JSON formatter on it
    # This ensures all logs go through the structlog pipeline
    handler = logging.StreamHandler(sys.stdout)
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processor=renderer,
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    # Suppress noisy logs from other libraries if needed
    logging.getLogger("uvicorn.access").disabled = True

    logger = structlog.get_logger("financial_agent")
    logger.info("✅Structured logging configured successfully.")
