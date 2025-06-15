import asyncio
import os
from typing import Any, AsyncGenerator, Iterator

from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage
from structlog import get_logger

from src.agents.stock_agent import StockAgent
from src.models.models import AgentDisplayConfig
from src.prompts.stock_market_prompts import agent_prompts
from src.services.message_parser import parse_agent_step
from src.tools.tools import (get_current_datetime,
                             retrieve_historical_stock_price,
                             retrieve_realtime_stock_price)

logger = get_logger()


def get_stock_agent_stream(query: str) -> Iterator[dict[str, Any] | Any]:
    """
    Initializes and runs a streaming agent session based on the user's query.

    This function prepares the agent environment by:
    - Formatting the user's input into the expected message format
    - Assembling the list of available tools (e.g., real-time stock, historical prices, datetime)
    - Binding those tools to the Bedrock-compatible LLM
    - Creating a configured `StockAgent` instance with the selected prompt
    - Returning a generator/iterator that streams intermediate steps of agent reasoning

    Args:
        query (str): The user's natural language question to be processed by the agent.

    Returns:
        Iterator[dict[str, Any] | Any]: A generator that yields structured steps or messages
        from the agent as it processes the query. This is typically consumed for real-time
        display or progressive output in a frontend or CLI.

    Example:
        for step in get_agent_stream("What was Apple's stock price last week?"):
            print(step)
    """

    # Format query
    initial_state = {"messages": [HumanMessage(content=query)]}

    # Gather tools
    tools = [
        retrieve_realtime_stock_price,
        retrieve_historical_stock_price,
        get_current_datetime]

    # LLM Configuration
    model = ChatBedrockConverse(
        model=os.getenv(
            "AWS_BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
    ).bind_tools(tools)

    # Create the agent
    agent = StockAgent(
        model=model,
        tools=tools,
        system_prompt=agent_prompts["v1"]
    )

    return agent.graph_app.stream(initial_state)


async def generate_agent_output(query: str) -> AsyncGenerator[str, None]:
    """
    Asynchronously streams parsed agent responses for a given query.

    This function runs the agent in a background thread, parses each reasoning step,
    and yields formatted message chunks suitable for real-time display.

    Args:
        query (str): The user's natural language query.

    Yields:
        str: Formatted text output from each agent step, streamed incrementally.
    """
    logger.bind(query=query).debug("🏁 Starting agent response stream")
    loop = asyncio.get_event_loop()

    def sync_generator():
        for step in get_stock_agent_stream(query):
            logger.bind(step=step).debug("⚡Processing agent step")
            yield from parse_agent_step(step, AgentDisplayConfig().from_env())

    gen = sync_generator()

    while True:
        chunk = await loop.run_in_executor(None, lambda: next(gen, None))
        if chunk is None:
            logger.info("😎 Finished streaming agent response")
            break
        logger.bind(chunk=chunk).debug("🚀 Streaming chunk")
        yield chunk
        await asyncio.sleep(0.01)
