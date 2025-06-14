from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from src.models.models import AgentRequest
from src.utils.auth import get_api_key
from src.services.agent_streaming import generate_agent_output

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
    if not request.query:
        raise HTTPException(status_code=400, detail="Query is required")

    return StreamingResponse(
        generate_agent_output(request.query),
        media_type="text/event-stream"
    )
