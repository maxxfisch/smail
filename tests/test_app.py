from fastapi.testclient import TestClient
import pytest
from app import app, conversation_history

@pytest.fixture
def client():
    return TestClient(app)

def test_root_no_session(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "chat_history" in response.context
    assert response.context["chat_history"] == []

def test_root_with_session_no_history(client):
    response = client.get("/", cookies={"session": "test_session"})
    assert response.status_code == 200
    assert "chat_history" in response.context
    assert response.context["chat_history"] == []

def test_root_with_session_and_history(client):
    # Add some test messages
    session_id = "test_session"
    conversation_history.add_message(session_id, "user", "Test message")
    conversation_history.add_message(session_id, "assistant", "Test response")
    
    response = client.get("/", cookies={"session": session_id})
    assert response.status_code == 200
    assert "chat_history" in response.context
    
    history = response.context["chat_history"]
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Test message"
    assert history[1]["role"] == "bot"
    assert history[1]["content"] == "Test response"

def test_chat_creates_session_if_none(client):
    response = client.post(
        "/chat",
        data={"message": "Hello"},
    )
    assert response.status_code == 200
    assert "session" in response.cookies

def test_chat_uses_existing_session(client):
    session_id = "existing_session"
    response = client.post(
        "/chat",
        data={"message": "Hello"},
        cookies={"session": session_id}
    )
    assert response.status_code == 200
    assert response.cookies.get("session") is None  # Should not set new session

def test_chat_adds_to_conversation_history(client):
    session_id = "test_session"
    message = "Test message"
    
    response = client.post(
        "/chat",
        data={"message": message},
        cookies={"session": session_id}
    )
    
    assert response.status_code == 200
    history = conversation_history.get_messages(session_id)
    assert len(history) > 0
    assert history[0]["role"] == "user"
    assert history[0]["content"] == message