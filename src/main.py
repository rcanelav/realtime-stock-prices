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
from src.agents.stock_agent import agent_app
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


@app.post("/api/stock-agent/invoke", dependencies=[Depends(get_api_key)])
async def invoke(request: AgentRequest):
    """
    Receives a query and streams the agent's response.
    The stream includes intermediate steps like tool calls and final output.
    """
    if not request.query:
        raise HTTPException(status_code=400, detail="Query is required")

    logger.info("📥 Received query", query=request.query)

    initial_state = {"messages": [HumanMessage(content=request.query)]}

    async def stream_response() -> AsyncGenerator[str, None]:
        loop = asyncio.get_event_loop()

        def sync_stream():
            for step in agent_app.stream(initial_state):
                # Handle both tool and model messages
                messages = (
                    step.get("reasoner", {}).get("messages", [])
                    or step.get("messages", [])
                )
                for msg in messages:
                    if isinstance(msg, ToolMessage):
                        yield f"[Tool Response] {msg.content}\n"
                    elif isinstance(msg, AIMessage):
                        if msg.content:
                            yield f"[AI] {msg.content}\n"
                        elif msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                tool_name = tool_call.get("name")
                                tool_input = tool_call.get("input")
                                yield f"[Tool Call] {tool_name} with input {tool_input}\n"
                    elif isinstance(msg, BaseMessage) and getattr(msg, "content", None):
                        yield f"{msg.content}\n"

        # Run sync generator in executor, then yield each part
        for chunk in await loop.run_in_executor(None, sync_stream):
            yield chunk
            await asyncio.sleep(0.05)

    return StreamingResponse(stream_response(), media_type="text/event-stream")


@app.get("/health")
async def healtcheck():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
