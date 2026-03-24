# tests/test_api.py
import pytest

from api import app, get_service
from fastapi.testclient import TestClient


class FakeChatService:
    async def ainvoke(self, message: str, thread_id: str):
        return f"Echo: {message}"


@pytest.fixture(scope="module")     # Uses the same client for all the tests (20s to 10s imporovement)
def client():
    fake_service = FakeChatService()
    app.dependency_overrides[get_service] = lambda: fake_service

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


class TestChatEndpoint:
    """Test the /chat endpoint."""
    
    def test_chat_success(self, client):
        """Test successful chat request."""
        response = client.post(
            "/chat",
            json={"message": "Hello", "thread_id": "test-123"}
        )
        assert response.status_code == 200
        assert "response" in response.json()
    
    def test_chat_missing_message(self, client):
        """Test chat with missing required field."""
        response = client.post(
            "/chat",
            json={"thread_id": "test-123"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_chat_empty_message(self, client):
        """Test chat with empty message."""
        response = client.post(
            "/chat",
            json={"message": "", "thread_id": "test-123"}
        )
        assert response.status_code == 422 

class TestLivenessEndpoint:
    """Test the /liveness endpoint."""
    
    def test_liveness_up(self, client):
        """Test that liveness endpoint returns healthy status."""
        response = client.get("/liveness")
        assert response.status_code == 200
        assert response.json() == {"message": "OK"}  # Adjust to your response
    
    def test_liveness_response_structure(self, client):
        """Test liveness response has expected structure."""
        response = client.get("/liveness")
        data = response.json()
        assert "message" in data
