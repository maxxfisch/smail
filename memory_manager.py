import chromadb
from chromadb.config import Settings
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

class MemoryManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.memory_dir = os.path.join(data_dir, "memory")
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=self.memory_dir)
        
        # Create or get collections for different types of memories
        self.conversations = self.client.get_or_create_collection(
            name="conversations",
            metadata={"description": "Past conversations with the assistant"}
        )
        
        self.facts = self.client.get_or_create_collection(
            name="facts",
            metadata={"description": "Important facts and information learned about the user"}
        )

    def add_conversation(self, session_id: str, user_message: str, assistant_response: str) -> None:
        """Store a conversation exchange in the vector database."""
        # Create a combined message for context
        full_exchange = f"User: {user_message}\nAssistant: {assistant_response}"
        
        # Add to ChromaDB with metadata
        self.conversations.add(
            documents=[full_exchange],
            metadatas=[{
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "type": "conversation"
            }],
            ids=[f"conv_{datetime.now().timestamp()}"]
        )

    def add_fact(self, fact: str, category: str) -> None:
        """Store an important fact about the user."""
        self.facts.add(
            documents=[fact],
            metadatas=[{
                "category": category,
                "timestamp": datetime.now().isoformat(),
                "type": "fact"
            }],
            ids=[f"fact_{datetime.now().timestamp()}"]
        )

    def get_relevant_memories(self, query: str, limit: int = 5) -> Dict[str, List[str]]:
        """Retrieve relevant memories based on the current context."""
        # Search both collections
        conv_results = self.conversations.query(
            query_texts=[query],
            n_results=limit
        )
        
        fact_results = self.facts.query(
            query_texts=[query],
            n_results=limit
        )
        
        return {
            "conversations": conv_results["documents"][0] if conv_results["documents"] else [],
            "facts": fact_results["documents"][0] if fact_results["documents"] else []
        }

    def extract_facts_from_conversation(self, user_message: str, assistant_response: str) -> List[str]:
        """Extract potential facts from conversations using simple heuristics."""
        facts = []
        
        # Look for statements about preferences, habits, or personal information
        lower_msg = user_message.lower()
        if any(keyword in lower_msg for keyword in ["i am", "i'm", "i like", "i prefer", "my", "i have"]):
            facts.append(user_message)
        
        return facts

    def get_context_for_prompt(self, current_message: str) -> str:
        """Generate a context string from relevant memories."""
        memories = self.get_relevant_memories(current_message)
        
        context_parts = []
        
        if memories["facts"]:
            context_parts.append("Relevant facts about me:")
            context_parts.extend(f"- {fact}" for fact in memories["facts"])
        
        if memories["conversations"]:
            context_parts.append("\nRelevant past conversations:")
            context_parts.extend(f"- {conv}" for conv in memories["conversations"])
        
        return "\n".join(context_parts)