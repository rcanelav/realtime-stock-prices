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
