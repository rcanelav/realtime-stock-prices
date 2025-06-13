import asyncio
from typing import AsyncGenerator
from langchain_core.messages import HumanMessage
from src.agents.stock_agent import agent_app
from src.services.message_parser import parse_agent_step


async def run_stock_agent(query: str) -> AsyncGenerator[str, None]:
    """Run the stock agent with the provided query.

    Args:
        query (str): The query to be processed by the agent.

    Yields:
        AsyncGenerator[str, None]: A generator that yields strings as the agent processes the query.

    """
    loop = asyncio.get_event_loop()
    initial_state = {"messages": [HumanMessage(content=query)]}

    def sync_stream():
        for step in agent_app.stream(initial_state):
            yield from parse_agent_step(step)

    for chunk in await loop.run_in_executor(None, lambda: list(sync_stream())):
        yield chunk
        await asyncio.sleep(0.05)
