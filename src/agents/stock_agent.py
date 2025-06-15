from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from structlog import get_logger

from src.models.models import AgentState

logger = get_logger()

load_dotenv()


class StockAgent:
    """
    This agent is designed to:
    - Accept user input as a sequence of messages
    - Invoke an LLM (via Bedrock or other compatible model) with optional system prompt context
    - Call tools when required (e.g., real-time stock retrieval)
    - Stream intermediate reasoning steps and results

    The agent is composed of a stateful LangGraph workflow with:
    - An LLM node (`llm`) that handles message generation
    - A tool node (`tools`) that executes tool calls (e.g., for data retrieval)
    - Conditional transitions based on tool usage

    Args:
        model: The language model instance, compatible with LangChain/Bedrock interfaces.
        tools (list[Callable]): List of callable tool functions available to the agent.
        system_prompt (str): Optional system prompt injected before user messages.
    """

    def __init__(self, model, tools, system_prompt):
        self.system_prompt = system_prompt
        self.model = model
        graph = StateGraph(AgentState)
        graph.add_node("llm", self._call_llm)
        graph.add_node("tools", ToolNode(tools))
        graph.add_edge(START, "llm")
        graph.add_conditional_edges(
            "llm",
            tools_condition,
        )
        graph.add_edge("tools", "llm")
        graph.add_edge("llm", END)
        self.graph_app = graph.compile()
        if hasattr(self.model, "bind_tools"):
            self.model = self.model.bind_tools(tools)

    def _call_llm(self, state: AgentState):
        """
        Invokes the LLM with the current message history, prepending a system prompt if provided.

        Args:
            state (AgentState): The current agent state containing the message history.

        Returns:
            dict: A dictionary with a single key `"messages"` containing the LLM response message.
        """
        logger.bind(state=state).debug("🛸 Preparing messages for LLM")
        messages = state["messages"]

        if self.system_prompt:
            messages = [SystemMessage(content=self.system_prompt)] + messages

        response = self.model.invoke(messages)
        logger.bind(response=response).info("🛸 LLM response")

        return {
            "messages": [response],
        }
