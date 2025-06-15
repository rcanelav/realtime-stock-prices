import unittest
from unittest.mock import MagicMock, patch

from src.agents.stock_agent import StockAgent
from src.models.models import AgentState


class TestStockAgent(unittest.TestCase):

    @patch("src.agents.stock_agent.StateGraph")
    @patch("src.agents.stock_agent.ToolNode")
    def test_initialization_binds_tools_and_builds_graph(self, mock_tool_node, mock_state_graph):
        mock_model = MagicMock()
        mock_bound_model = MagicMock()
        mock_model.bind_tools.return_value = mock_bound_model

        mock_graph = MagicMock()
        mock_state_graph.return_value = mock_graph
        mock_graph.compile.return_value = "mock_graph_app"

        tools = [lambda: "tool1", lambda: "tool2"]
        agent = StockAgent(model=mock_model, tools=tools,
                           system_prompt="You are a bot")

        # Check tools were bound
        mock_model.bind_tools.assert_called_once_with(tools)
        self.assertEqual(agent.model, mock_bound_model)

        # Check graph was constructed correctly
        self.assertEqual(agent.graph_app, "mock_graph_app")
        mock_graph.add_node.assert_any_call("llm", agent._call_llm)
        mock_graph.add_node.assert_any_call(
            "tools", mock_tool_node.return_value)
        mock_graph.add_edge.assert_any_call("tools", "llm")

    def test_call_llm_with_and_without_system_prompt(self):
        # Case 1: With system prompt
        mock_model = MagicMock()
        mock_bound_model = MagicMock()
        mock_model.bind_tools.return_value = mock_bound_model

        agent_with_prompt = StockAgent(
            model=mock_model, tools=[], system_prompt="Be smart.")
        state = AgentState(messages=[MagicMock()])
        mock_bound_model.invoke.return_value = MagicMock()

        result = agent_with_prompt._call_llm(state)

        mock_bound_model.invoke.assert_called_once()
        passed_msgs = mock_bound_model.invoke.call_args[0][0]
        assert passed_msgs[0].content == "Be smart."
        assert "messages" in result

        # Case 2: Without system prompt
        mock_model2 = MagicMock()
        mock_bound_model2 = MagicMock()
        mock_model2.bind_tools.return_value = mock_bound_model2

        agent_no_prompt = StockAgent(
            model=mock_model2, tools=[], system_prompt=None)
        mock_bound_model2.invoke.return_value = MagicMock()

        _ = agent_no_prompt._call_llm(state)

        mock_bound_model2.invoke.assert_called_once()
        passed_msgs2 = mock_bound_model2.invoke.call_args[0][0]
        assert passed_msgs2[0] == state["messages"][0]


if __name__ == "__main__":
    unittest.main()
