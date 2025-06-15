from unittest.mock import MagicMock, patch

import pytest

from src.services.agent_streaming import (generate_agent_output,
                                          get_stock_agent_stream)


class TestGetStockAgentStream:

    @patch("src.services.agent_streaming.StockAgent")
    @patch("src.services.agent_streaming.ChatBedrockConverse")
    def test_get_stock_agent_stream_returns_generator(self, mock_bedrock, mock_stock_agent):
        # Arrange
        mock_stream = MagicMock()
        mock_stream.stream.return_value = iter([{"mock": "step1"}, {"mock": "step2"}])

        mock_stock_agent.return_value.graph_app = mock_stream
        mock_bedrock.return_value.bind_tools.return_value = MagicMock()

        # Act
        result = get_stock_agent_stream("Test query")

        # Assert
        assert iter(result)
        steps = list(result)
        assert len(steps) == 2
        assert steps[0]["mock"] == "step1"


class TestGenerateAgentOutput:

    @pytest.mark.asyncio
    @patch("src.services.agent_streaming.parse_agent_step")
    @patch("src.services.agent_streaming.get_stock_agent_stream")
    async def test_generate_agent_output_streams_correctly(self, mock_stream, mock_parse):
        # Arrange
        mock_stream.return_value = iter([
            {"step": 1},
            {"step": 2}
        ])
        mock_parse.side_effect = lambda step, _: [f"parsed-{step['step']}"]

        # Act
        output = []
        async for chunk in generate_agent_output("Test query"):
            output.append(chunk)

        # Assert
        assert output == ["parsed-1", "parsed-2"]
        assert mock_parse.call_count == 2

    @pytest.mark.asyncio
    @patch("src.services.agent_streaming.parse_agent_step")
    @patch("src.services.agent_streaming.get_stock_agent_stream")
    async def test_generate_agent_output_handles_empty(self, mock_stream, mock_parse):
        # Arrange
        mock_stream.return_value = iter([])
        mock_parse.return_value = []

        # Act
        output = []
        async for chunk in generate_agent_output("No steps"):
            output.append(chunk)

        # Assert
        assert output == []
        mock_parse.assert_not_called()
