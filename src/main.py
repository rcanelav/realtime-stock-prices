import asyncio
import os
from asyncio import sleep
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, Security, status
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader
from langchain_core.messages import (AIMessage, BaseMessage, HumanMessage,
                                     ToolMessage)

from src.models.models import AgentRequest
from src.tools.agent import agent_app
from src.utils.logging_config import setup_logging

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
logger = structlog.get_logger(__name__)


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
    title="Financial agent API",
    description="An API for processing financial queries using AWS BEDROCK with streaming responses.",
    lifespan=lifespan
)


async def get_api_key(api_key: str = Security(api_key_header)):
    """Dependency to validate the API key."""
    expected_api_key = os.getenv("SERVICE_API_KEY")
    if api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )


async def process_query(query: str):
    # Simulate processing the query
    import asyncio
    for i in range(300):
        await asyncio.sleep(1)  # Simulate a delay
        yield f"Processing chunk {i + 1} for query: {query}"
    yield "Query processing complete."


@app.post("/api/invoke")
async def main(request: Request):
    data = await request.json()
    query = data.get("query", "")
    if not query:
        return {"error": "No query provided"}

    async def stream():
        async for chunk in process_query(query):
            yield chunk + "\n"
            await sleep(0.1)
    return StreamingResponse(stream(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
