import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.security import APIKeyHeader
from structlog import get_logger

from src.routes import dummy, stock_agent
from src.utils.logging_config import setup_logging

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the application.
    This function is called when the application starts up and shuts down.

    Args:
        app (FastAPI): The FastAPI application instance.

    Raises:
        RuntimeError: If the AWS_REGION or SERVICE_API_KEY environment variables are not set.
    """
    # Initialize logging
    setup_logging()

    # Load environment variables
    load_dotenv()
    if not os.getenv("AWS_REGION"):
        logger.error("env_var_missing", var_name="AWS_REGION")
        raise RuntimeError("AWS_REGION environment variable not set.")
    if not os.getenv("SERVICE_API_KEY"):
        logger.error("env_var_missing", var_name="SERVICE_API_KEY")
        raise RuntimeError("SERVICE_API_KEY environment variable not set.")

    logger.info("✅Application startup complete.")
    yield

# App initialization
app = FastAPI(
    title="Stock market agent API",
    description="An API for processing stock market related queries using AWS BEDROCK with streaming responses.",
    lifespan=lifespan
)

# Routes
app.include_router(stock_agent.router, prefix="/api")
app.include_router(dummy.router, prefix="/api")
app.add_api_route("/health", lambda: {"status": "ok"}, methods=["GET"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
