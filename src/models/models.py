import operator
import os
from dataclasses import dataclass
from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field

# ########################################################################
#                           Models
# ########################################################################


class AgentRequest(BaseModel):
    """
    Request model for interacting with the agent via FastAPI.

    This model represents the expected payload structure when a client sends a query
    to the agent endpoint.

    Attributes:
        query (str): The natural language question or instruction provided by the user.
                     This string will be processed by the agent to generate a response.

    Example request body:
        {
            "query": "What is the current stock price of Tesla?"
        }
    """
    query: str


class TickerInput(BaseModel):
    """Input model for any tool that requires a stock ticker."""
    ticker: str = Field(...,
                        description="The stock ticker symbol, e.g., 'AAPL' for Apple.")


class EmptyInput(BaseModel):
    """This tool takes no input."""


class AgentState(TypedDict):
    """
    Represents the evolving state of the agent throughout a LangGraph workflow.

    This state is passed between nodes in the graph and accumulates messages over time,
    such as user inputs, system prompts, tool calls, and AI responses.

    Attributes:
        messages (list[AnyMessage]):
            A list of message objects exchanged during the agent's reasoning process.
            This includes all interaction types (e.g., HumanMessage, AIMessage, ToolMessage).

            The Annotated operator (operator.add) tells LangGraph how to merge state across steps.
            In this case, new messages are appended to the existing list using the '+' operator.

    Example:
        {
            "messages": [
                HumanMessage(content="What's the weather today?"),
                AIMessage(content="Let me check..."),
                ToolMessage(content="72°F and sunny")
            ]
        }

    Note:
        This model is used as the state definition in StateGraph(...), and is essential for
        enabling message accumulation and loop-based workflows in LangGraph.
    """
    messages: Annotated[list[AnyMessage], operator.add]


@dataclass
class AgentDisplayConfig:
    """
    Configuration for controlling which types of agent messages are displayed.

    You can control the flags by setting environment variables at runtime:
    - SHOW_TOOL_CALLS
    - SHOW_TOOL_RESPONSES
    - SHOW_AI_MESSAGES
    - SHOW_BASE_MESSAGES

    Accepted values for each flag (case-insensitive): "1", "true", "yes", "on" → True.
    Anything else will be interpreted as False.

    By default, all flags are set to True. These defaults can be changed in two ways:
    1. **Via environment variables** using `AgentDisplayConfig.from_env()`.
       Example: `SHOW_TOOL_CALLS=false python run.py`
    2. **By directly hardcoding new defaults** in the dataclass itself.
       Modifying the default values in the class definition (e.g., `show_tool_calls=False`)
       will only apply when instantiating `AgentDisplayConfig()` directly — **not** when using `from_env()`.

    Note: If you use `from_env()`, environment variables override the class defaults.
    """
    show_tool_calls: bool = True
    show_tool_responses: bool = True
    show_ai_messages: bool = True
    show_base_messages: bool = True

    @classmethod
    def from_env(cls) -> "AgentDisplayConfig":
        def env_bool(var: str, default: bool) -> bool:
            return os.getenv(var, str(default)).lower() in ("1", "true", "yes", "on")

        return cls(
            show_tool_calls=env_bool("SHOW_TOOL_CALLS", True),
            show_tool_responses=env_bool("SHOW_TOOL_RESPONSES", True),
            show_ai_messages=env_bool("SHOW_AI_MESSAGES", True),
            show_base_messages=env_bool("SHOW_BASE_MESSAGES", True),
        )
