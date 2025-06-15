from unittest.mock import patch
import os
import pytest
from src.main import lifespan
from fastapi import FastAPI


@pytest.mark.asyncio
class TestLifespan:

    def setup_method(self):
        self.original_env = {
            "AWS_REGION": os.getenv("AWS_REGION"),
            "SERVICE_API_KEY": os.getenv("SERVICE_API_KEY")
        }

    def teardown_method(self):
        for key, value in self.original_env.items():
            if value is not None:
                os.environ[key] = value
            else:
                os.environ.pop(key, None)

    async def test_successful_lifespan_startup(self, monkeypatch):
        monkeypatch.setenv("AWS_REGION", "us-east-1")
        monkeypatch.setenv("SERVICE_API_KEY", "test-key")

        # Prevent load_dotenv from actually loading .env files
        with patch("src.main.load_dotenv", return_value=None):
            async with lifespan(FastAPI()) as _:
                assert True

    async def test_missing_aws_region(self, monkeypatch):
        monkeypatch.delenv("AWS_REGION", raising=False)
        monkeypatch.setenv("SERVICE_API_KEY", "test-key")

        with patch("src.main.load_dotenv", return_value=None):
            with pytest.raises(RuntimeError, match="AWS_REGION environment variable not set"):
                async with lifespan(FastAPI()):
                    pass

    async def test_missing_service_api_key(self, monkeypatch):
        monkeypatch.setenv("AWS_REGION", "us-east-1")
        monkeypatch.delenv("SERVICE_API_KEY", raising=False)

        with patch("src.main.load_dotenv", return_value=None):
            with pytest.raises(RuntimeError, match="SERVICE_API_KEY environment variable not set"):
                async with lifespan(FastAPI()):
                    pass
