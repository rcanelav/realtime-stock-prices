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

# LLM Configuration
model = ChatBedrockConverse(model=os.getenv(
    "AWS_BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"),
).bind_tools(tools)

# System prompt for the agent
system_message = SystemMessage(
    content="""
        You are a financial agent that can answer questions about stock prices.
        You have access to tools for real-time prices, historical prices, and current datetime.
        "If a user asks about relative time ranges like 'Q4 last year', 'last week', or 'today',
        "use the current datetime tool first to determine the correct date range before retrieving stock data."""
)


def reasoner(state: MessagesState):
    return {
        "messages": [model.invoke([system_message] + state['messages'])],
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
