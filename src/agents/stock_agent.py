from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from structlog import get_logger

from src.models.models import AgentState

logger = get_logger()

load_dotenv()


class StockAgent:
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

        logger.bind(state=state).debug("🛸 Preparing messages for LLM")
        messages = state['messages']

        if self.system_prompt:
            messages = [SystemMessage(content=self.system_prompt)] + messages

        response = self.model.invoke(messages)
        logger.bind(response=response).info("🛸 LLM response")

        return {
            "messages": [response],
        }
