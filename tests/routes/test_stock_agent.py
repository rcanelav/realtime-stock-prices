from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app
from src.routes import stock_agent

client = TestClient(app)
VALID_API_KEY = "test-key"


class TestStockAgentInvoke:

    def setup_method(self):
        # Override API key dependency to bypass actual validation
        app.dependency_overrides[stock_agent.get_api_key] = lambda: None

    def teardown_method(self):
        app.dependency_overrides = {}

    @patch("src.routes.stock_agent.generate_agent_output")
    def test_streaming_success(self, mock_generate):
        async def mock_stream():
            yield "data: This is a mock stream\n\n"

        mock_generate.return_value = mock_stream()

        response = client.post(
            "/api/stock-agent/invoke",
            headers={"X-API-KEY": VALID_API_KEY},
            json={"query": "What's the price of AAPL?"}
        )

        assert response.status_code == 200
        assert "data: This is a mock stream" in response.text
