from unittest.mock import MagicMock

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage

from src.models.models import AgentDisplayConfig
from src.services.message_parser import _format_msg, parse_agent_step


class TestParseAgentStep:

    def test_parses_valid_step_with_ai_message(self):
        step = {
            "llm": {
                "messages": [
                    AIMessage(content="Hello\nHow are you?", tool_calls=[])
                ]
            }
        }
        config = AgentDisplayConfig(
            show_ai_messages=True,
            show_tool_calls=False,
            show_tool_responses=False,
            show_base_messages=False
        )

        result = parse_agent_step(step, config)
        assert result == [
            "[LLM] [AI] Hello\n",
            "[LLM] [AI] How are you?\n"
        ]

    def test_skips_invalid_node_output(self):
        step = {
            "invalid_node": {"unexpected_key": "no messages"}
        }
        config = AgentDisplayConfig()
        result = parse_agent_step(step, config)
        assert result == []

    def test_parses_multiple_nodes(self):
        step = {
            "llm": {
                "messages": [
                    AIMessage(content="llm step", tool_calls=[])
                ]
            },
            "tool_use": {
                "messages": [
                    ToolMessage(content="Tool result", tool_call_id="tool1")
                ]
            }
        }
        config = AgentDisplayConfig(
            show_ai_messages=True,
            show_tool_calls=False,
            show_tool_responses=True,
            show_base_messages=False
        )

        result = parse_agent_step(step, config)
        assert "[LLM] [AI] llm step\n" in result
        assert "[TOOL_USE] [Tool Response] Tool result\n" in result


class TestFormatMsg:

    def test_tool_message_with_response(self):
        msg = ToolMessage(content="Tool did something", tool_call_id="abc")
        config = AgentDisplayConfig(show_tool_responses=True)
        result = _format_msg(msg, "[TOOL]", config)
        assert result == ["[TOOL] [Tool Response] Tool did something\n"]

    def test_ai_message_with_lines_and_tool_call(self):
        mock_msg = MagicMock(spec=AIMessage)
        mock_msg.content = "Line 1\nLine 2"
        mock_msg.tool_calls = [
            {"name": "fetch_stock", "input": {"symbol": "AAPL"}}]

        config = AgentDisplayConfig(
            show_ai_messages=True,
            show_tool_calls=True
        )
        result = _format_msg(mock_msg, "[LLM]", config)

        assert "[LLM] [AI] Line 1\n" in result
        assert "[LLM] [AI] Line 2\n" in result
        assert '[LLM] [Tool Call] fetch_stock with input {\n  "symbol": "AAPL"\n}\n' in result

    def test_base_message_with_content(self):
        msg = BaseMessage(content="Base message!", type="human")
        config = AgentDisplayConfig(show_base_messages=True)
        result = _format_msg(msg, "[BASE]", config)
        assert result == ["[BASE] Base message!\n"]

    def test_message_with_list_content(self):
        msg = AIMessage(
            content=[{"text": "Part 1 "}, {"text": "Part 2"}],
            tool_calls=[]
        )
        config = AgentDisplayConfig(show_ai_messages=True)
        result = _format_msg(msg, "[LLM]", config)
        assert result == ["[LLM] [AI] Part 1 Part 2\n"]
