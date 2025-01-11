import os
import tempfile
import shutil
from datetime import datetime
import pytest
from unittest.mock import MagicMock, patch
from memory_manager import MemoryManager

@pytest.fixture
def temp_data_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_chroma():
    with patch('chromadb.PersistentClient') as mock_client:
        mock_conversations = MagicMock()
        mock_facts = MagicMock()
        
        # Setup mock collections
        mock_client.return_value.get_or_create_collection.side_effect = [
            mock_conversations,  # First call for conversations
            mock_facts          # Second call for facts
        ]
        
        yield {
            'client': mock_client,
            'conversations': mock_conversations,
            'facts': mock_facts
        }

@pytest.fixture
def memory_manager(temp_data_dir, mock_chroma):
    return MemoryManager(data_dir=temp_data_dir)

def test_init_creates_memory_dir(temp_data_dir):
    MemoryManager(data_dir=temp_data_dir)
    memory_dir = os.path.join(temp_data_dir, "memory")
    assert os.path.exists(memory_dir)

def test_add_conversation(memory_manager, mock_chroma):
    session_id = "test_session"
    user_message = "Hello"
    assistant_response = "Hi there!"
    
    memory_manager.add_conversation(session_id, user_message, assistant_response)
    
    mock_chroma['conversations'].add.assert_called_once()
    call_args = mock_chroma['conversations'].add.call_args[1]
    
    assert len(call_args['documents']) == 1
    assert call_args['documents'][0] == f"User: {user_message}\nAssistant: {assistant_response}"
    assert call_args['metadatas'][0]['session_id'] == session_id
    assert call_args['metadatas'][0]['type'] == "conversation"
    assert len(call_args['ids'][0]) > 0

def test_add_fact(memory_manager, mock_chroma):
    fact = {
        "content": "I like programming",
        "category": "preference",
        "source": "user_message",
        "confidence": "medium",
        "timestamp": datetime.now().isoformat()
    }
    
    memory_manager.add_fact(fact)
    
    mock_chroma['facts'].add.assert_called_once()
    call_args = mock_chroma['facts'].add.call_args[1]
    
    assert call_args['documents'][0] == fact["content"]
    assert call_args['metadatas'][0]['category'] == fact["category"]
    assert call_args['metadatas'][0]['source'] == fact["source"]
    assert call_args['metadatas'][0]['confidence'] == fact["confidence"]
    assert call_args['metadatas'][0]['timestamp'] == fact["timestamp"]
    assert len(call_args['ids'][0]) > 0

def test_get_relevant_memories(memory_manager, mock_chroma):
    query = "test query"
    mock_conv_results = {
        "documents": [["Past conversation 1", "Past conversation 2"]],
    }
    mock_fact_results = {
        "documents": [["Fact 1", "Fact 2"]],
    }
    
    memory_manager.conversations.query.return_value = mock_conv_results
    memory_manager.facts.query.return_value = mock_fact_results
    
    memories = memory_manager.get_relevant_memories(query, limit=2)
    
    assert memories["conversations"] == ["Past conversation 1", "Past conversation 2"]
    assert memories["facts"] == ["Fact 1", "Fact 2"]
    
    memory_manager.conversations.query.assert_called_once_with(
        query_texts=[query], n_results=2
    )
    memory_manager.facts.query.assert_called_once_with(
        query_texts=[query], n_results=2
    )

def test_extract_facts_from_conversation_user_preferences():
    manager = MemoryManager()
    user_message = "I like programming. I enjoy reading books. I hate spicy food."
    assistant_response = ""
    
    facts = manager.extract_facts_from_conversation(user_message, assistant_response)
    
    # The implementation extracts facts based on complete sentences containing the patterns
    preferences = [f for f in facts if f["category"] == "preference"]
    assert len(preferences) == 3
    
    contents = [f["content"].strip() for f in preferences]
    assert "I like programming" in contents
    assert "I enjoy reading books" in contents
    assert "I hate spicy food" in contents

def test_extract_facts_from_conversation_personal_info():
    manager = MemoryManager()
    user_message = "I am a software developer. I live in New York."
    assistant_response = ""
    
    facts = manager.extract_facts_from_conversation(user_message, assistant_response)
    
    # The implementation extracts facts based on complete sentences containing the patterns
    personal_info = [f for f in facts if f["category"] == "personal_info"]
    assert len(personal_info) == 2
    
    contents = [f["content"].strip() for f in personal_info]
    assert "I am a software developer" in contents
    assert "I live in New York" in contents

def test_extract_facts_from_conversation_assistant_confirmation():
    manager = MemoryManager()
    user_message = "Just a regular message"
    assistant_response = "As you told me before, you are a software developer."
    
    facts = manager.extract_facts_from_conversation(user_message, assistant_response)
    
    assert len(facts) == 1
    assert facts[0]["category"] == "confirmation"
    assert "you told me" in facts[0]["content"].lower()
    assert facts[0]["source"] == "assistant_response"
    assert facts[0]["confidence"] == "medium"

def test_get_context_for_prompt(memory_manager, mock_chroma):
    query = "test query"
    mock_facts = ["I am a developer", "I live in New York"]
    mock_conversations = ["Previous conversation about work"]
    
    # Mock the facts collection get method
    memory_manager.facts.get.return_value = {
        "metadatas": [{"confidence": "high"}, {"confidence": "high"}]
    }
    
    # Mock query results
    memory_manager.get_relevant_memories = MagicMock(return_value={
        "facts": mock_facts,
        "conversations": mock_conversations
    })
    
    context = memory_manager.get_context_for_prompt(query)
    
    assert "I am a developer" in context
    assert "I live in New York" in context
    assert "Previous conversation about work" in context
    
    memory_manager.get_relevant_memories.assert_called_once_with(query, limit=3)