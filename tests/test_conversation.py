from datetime import datetime
from conversation import ConversationHistory

import tempfile
import shutil
import os
import json

@pytest.fixture
def temp_data_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_get_messages_empty(temp_data_dir):
    conv = ConversationHistory(data_dir=temp_data_dir)
    messages = conv.get_messages("test_session")
    assert messages == []

def test_get_messages_with_history(temp_data_dir):
    conv = ConversationHistory(data_dir=temp_data_dir)
    session_id = "test_session"
    
    # Add some test messages
    conv.add_message(session_id, "user", "Hello")
    conv.add_message(session_id, "assistant", "Hi there!")
    conv.add_message(session_id, "user", "How are you?")
    
    # Create a new instance to test persistence
    conv2 = ConversationHistory(data_dir=temp_data_dir)
    messages = conv2.get_messages(session_id)
    
    assert len(messages) == 3
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello"
    assert messages[1]["role"] == "bot"  # assistant should be mapped to bot
    assert messages[1]["content"] == "Hi there!"
    assert messages[2]["role"] == "user"
    assert messages[2]["content"] == "How are you?"
    
    # Verify the JSON file exists and contains the correct data
    conv_file = os.path.join(temp_data_dir, "conversations.json")
    assert os.path.exists(conv_file)
    with open(conv_file, 'r') as f:
        data = json.load(f)
        assert session_id in data
        assert len(data[session_id]) == 3

def test_get_messages_multiple_sessions(temp_data_dir):
    conv = ConversationHistory(data_dir=temp_data_dir)
    session1 = "session1"
    session2 = "session2"
    
    # Add messages to different sessions
    conv.add_message(session1, "user", "Hello from session 1")
    conv.add_message(session2, "user", "Hello from session 2")
    conv.add_message(session1, "assistant", "Hi session 1!")
    conv.add_message(session2, "assistant", "Hi session 2!")
    
    # Create a new instance to test persistence
    conv2 = ConversationHistory(data_dir=temp_data_dir)
    messages1 = conv2.get_messages(session1)
    messages2 = conv2.get_messages(session2)
    
    assert len(messages1) == 2
    assert len(messages2) == 2
    assert messages1[0]["content"] == "Hello from session 1"
    assert messages2[0]["content"] == "Hello from session 2"
    assert messages1[1]["content"] == "Hi session 1!"
    assert messages2[1]["content"] == "Hi session 2!"
    
    # Verify the JSON file contains both sessions
    conv_file = os.path.join(temp_data_dir, "conversations.json")
    with open(conv_file, 'r') as f:
        data = json.load(f)
        assert session1 in data
        assert session2 in data
        assert len(data[session1]) == 2
        assert len(data[session2]) == 2

def test_get_messages_respects_max_history(temp_data_dir):
    conv = ConversationHistory(max_history=2, data_dir=temp_data_dir)
    session_id = "test_session"
    
    # Add more messages than max_history
    conv.add_message(session_id, "user", "Message 1")
    conv.add_message(session_id, "assistant", "Response 1")
    conv.add_message(session_id, "user", "Message 2")
    conv.add_message(session_id, "assistant", "Response 2")
    
    # Create a new instance to test persistence
    conv2 = ConversationHistory(max_history=2, data_dir=temp_data_dir)
    messages = conv2.get_messages(session_id)
    
    assert len(messages) == 2
    assert messages[0]["content"] == "Message 2"
    assert messages[1]["content"] == "Response 2"
    
    # Verify the JSON file respects max_history
    conv_file = os.path.join(temp_data_dir, "conversations.json")
    with open(conv_file, 'r') as f:
        data = json.load(f)
        assert len(data[session_id]) == 2
        assert data[session_id][-2]["content"] == "Message 2"
        assert data[session_id][-1]["content"] == "Response 2"