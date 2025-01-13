from datetime import datetime
from conversation import ConversationHistory

def test_get_messages_empty():
    conv = ConversationHistory()
    messages = conv.get_messages("test_session")
    assert messages == []

def test_get_messages_with_history():
    conv = ConversationHistory()
    session_id = "test_session"
    
    # Add some test messages
    conv.add_message(session_id, "user", "Hello")
    conv.add_message(session_id, "assistant", "Hi there!")
    conv.add_message(session_id, "user", "How are you?")
    
    messages = conv.get_messages(session_id)
    
    assert len(messages) == 3
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello"
    assert messages[1]["role"] == "bot"  # assistant should be mapped to bot
    assert messages[1]["content"] == "Hi there!"
    assert messages[2]["role"] == "user"
    assert messages[2]["content"] == "How are you?"

def test_get_messages_multiple_sessions():
    conv = ConversationHistory()
    session1 = "session1"
    session2 = "session2"
    
    # Add messages to different sessions
    conv.add_message(session1, "user", "Hello from session 1")
    conv.add_message(session2, "user", "Hello from session 2")
    conv.add_message(session1, "assistant", "Hi session 1!")
    conv.add_message(session2, "assistant", "Hi session 2!")
    
    messages1 = conv.get_messages(session1)
    messages2 = conv.get_messages(session2)
    
    assert len(messages1) == 2
    assert len(messages2) == 2
    assert messages1[0]["content"] == "Hello from session 1"
    assert messages2[0]["content"] == "Hello from session 2"
    assert messages1[1]["content"] == "Hi session 1!"
    assert messages2[1]["content"] == "Hi session 2!"

def test_get_messages_respects_max_history():
    conv = ConversationHistory(max_history=2)
    session_id = "test_session"
    
    # Add more messages than max_history
    conv.add_message(session_id, "user", "Message 1")
    conv.add_message(session_id, "assistant", "Response 1")
    conv.add_message(session_id, "user", "Message 2")
    conv.add_message(session_id, "assistant", "Response 2")
    
    messages = conv.get_messages(session_id)
    
    assert len(messages) == 2
    assert messages[0]["content"] == "Message 2"
    assert messages[1]["content"] == "Response 2"