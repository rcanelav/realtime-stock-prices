
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from structlog import get_logger

from src.models.models import AgentRequest
from src.services.agent_streaming import generate_agent_output
from src.utils.auth import get_api_key

logger = get_logger()
router = APIRouter()


@router.post("/stock-agent/invoke", dependencies=[Depends(get_api_key)])
async def invoke(request: AgentRequest):
    """
    Endpoint to invoke the stock agent and stream its response.

    Accepts a natural language query in the request body and streams the agent's
    parsed responses back to the client using Server-Sent Events (SSE).

    Args:
        request (AgentRequest): The request payload containing the user's query.

    Returns:
        StreamingResponse: An SSE stream of the agent's response chunks (text/event-stream).

    Raises:
        HTTPException: If the query is missing or invalid.
    """
    logger.bind(query=request.query).debug("🛸 Processing stock-agent request")
    if not request.query:
        message = "Query missing in request body"
        logger.error(f"❌ {message}")
        raise HTTPException(status_code=400, detail=message)

    return StreamingResponse(
        generate_agent_output(request.query),
        media_type="text/event-stream"
    )
