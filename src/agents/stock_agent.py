import os

from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import SystemMessage
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from src.tools.tools import (get_current_datetime,
                             retrieve_historical_stock_price,
                             retrieve_realtime_stock_price)

load_dotenv()
# Group tools
tools = [
    retrieve_realtime_stock_price,
    retrieve_historical_stock_price,
    get_current_datetime]

tool_node = ToolNode(tools)


# System prompt for the agent
system_message = SystemMessage(
    content="""
        You are a financial assistant specialized in stock market data.

        You can answer questions related to:
        - Real-time stock prices
        - Historical stock prices
        - Current date and time

        You have access to the following tools:
        1. A tool to retrieve real-time stock prices for specific tickers.
        2. A tool to retrieve historical stock data for specified date ranges.
        3. A tool to get the current date and time.

        **Behavior Guidelines:**
        - If the user's query involves relative time expressions (e.g., “Q4 last year”, “last week”, “today”), always call the current datetime tool first to resolve the exact date range.
        - When retrieving data, ensure your response is clear, concise, and formatted in tables when appropriate.
        - If the question is unrelated to stock prices or market data, respond politely and decline to answer."""
)

# LLM Configuration
model = ChatBedrockConverse(
    model=os.getenv(
        "AWS_BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
).bind_tools(tools)

MAX_MESSAGES = 10


def reasoner(state: MessagesState):
    messages = state['messages']

    # Deduplicate system prompt
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [system_message] + messages

    # Truncate to avoid token explosion
    messages = messages[-MAX_MESSAGES:]

    return {
        "messages": [model.invoke(messages)],
    }


# ########################################################################
#                           TAgent Graph
# ########################################################################
agent_graph = StateGraph(MessagesState)
agent_graph.add_node("reasoner", reasoner)
agent_graph.add_node("tools", ToolNode(tools))
agent_graph.add_edge(START, "reasoner")
# if latest message from rsn is a tc, tools conditions routes to tools. Otherwise it routes to end
agent_graph.add_conditional_edges(
    "reasoner",
    tools_condition,
)

agent_graph.add_edge("tools", "reasoner")
agent_app = agent_graph.compile()
