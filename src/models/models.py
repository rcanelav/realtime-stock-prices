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
    query: str


class TickerInput(BaseModel):
    """Input model for any tool that requires a stock ticker."""
    ticker: str = Field(...,
                        description="The stock ticker symbol, e.g., 'AAPL' for Apple.")


class EmptyInput(BaseModel):
    """This tool takes no input."""


class AgentState(TypedDict):
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
