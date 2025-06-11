import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from asyncio import sleep
app = FastAPI()


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
