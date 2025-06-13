from asyncio import sleep
from typing import AsyncGenerator
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

router = APIRouter()


async def process_query(query: str) -> AsyncGenerator[str, None]:
    """Process the query and yield results in chunks.
    This function simulates processing a query by yielding chunks of data

    Args:
        query (str): The query to process.

    Yields:
        AsyncGenerator[str, None]: A generator that yields strings as the query is processed.
    """
    import asyncio
    for i in range(10):
        await asyncio.sleep(1)  # Simulate a delay
        yield f"Processing chunk {i + 1} for query: {query}"
    yield "Query processing complete."


@router.post("/invoke")
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
