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
    assert "session" in response.cookies  # Should set a new session cookie

def test_root_with_session_no_history(client):
    response = client.get("/", cookies={"session": "test_session"})
    assert response.status_code == 200
    assert "chat_history" in response.context
    assert response.context["chat_history"] == []

def test_root_with_session_and_history(client, temp_data_dir):
    # Create a conversation history with a test directory
    session_id = "test_session"
    conv = ConversationHistory(data_dir=temp_data_dir)
    app.conversation_history = conv  # Replace the app's conversation history
    
    # Add some test messages
    conv.add_message(session_id, "user", "Test message")
    conv.add_message(session_id, "assistant", "Test response")
    
    response = client.get("/", cookies={"session": session_id})
    assert response.status_code == 200
    assert "chat_history" in response.context
    
    history = response.context["chat_history"]
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Test message"
    assert history[1]["role"] == "bot"
    assert history[1]["content"] == "Test response"
    
    # Verify persistence
    conv_file = os.path.join(temp_data_dir, "conversations.json")
    assert os.path.exists(conv_file)
    with open(conv_file, 'r') as f:
        data = json.load(f)
        assert session_id in data
        assert len(data[session_id]) == 2

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

def test_chat_adds_to_conversation_history(client, temp_data_dir):
    # Setup test conversation history
    session_id = "test_session"
    conv = ConversationHistory(data_dir=temp_data_dir)
    app.conversation_history = conv
    
    message = "Test message"
    response = client.post(
        "/chat",
        data={"message": message},
        cookies={"session": session_id}
    )
    
    assert response.status_code == 200
    history = conv.get_messages(session_id)
    assert len(history) > 0
    assert history[0]["role"] == "user"
    assert history[0]["content"] == message
    
    # Verify persistence
    conv_file = os.path.join(temp_data_dir, "conversations.json")
    assert os.path.exists(conv_file)
    with open(conv_file, 'r') as f:
        data = json.load(f)
        assert session_id in data
        assert len(data[session_id]) > 0

def test_profile_route_session_handling(client):
    # Test without session
    response = client.get("/profile")
    assert response.status_code == 200
    assert "session" in response.cookies
    
    # Test with existing session
    session_id = "test_session"
    response = client.get("/profile", cookies={"session": session_id})
    assert response.status_code == 200
    assert "session" not in response.cookies  # Should not set new session

def test_memories_route_session_handling(client):
    # Test without session
    response = client.get("/memories")
    assert response.status_code == 200
    assert "session" in response.cookies
    
    # Test with existing session
    session_id = "test_session"
    response = client.get("/memories", cookies={"session": session_id})
    assert response.status_code == 200
    assert "session" not in response.cookies  # Should not set new session

def test_session_persistence_across_routes(client, temp_data_dir):
    # Setup test conversation history
    conv = ConversationHistory(data_dir=temp_data_dir)
    app.conversation_history = conv
    
    # Start at chat page
    response = client.get("/")
    assert response.status_code == 200
    session = response.cookies["session"]
    
    # Send a chat message
    message = "Test message"
    response = client.post(
        "/chat",
        data={"message": message},
        cookies={"session": session}
    )
    assert response.status_code == 200
    
    # Navigate to profile and back
    response = client.get("/profile", cookies={"session": session})
    assert response.status_code == 200
    
    response = client.get("/", cookies={"session": session})
    assert response.status_code == 200
    history = response.context["chat_history"]
    assert len(history) > 0
    assert history[0]["role"] == "user"
    assert history[0]["content"] == message