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

    def extract_facts_from_conversation(self, user_message: str, assistant_response: str) -> List[Dict[str, str]]:
        """Extract potential facts from conversations using advanced pattern matching."""
        facts = []
        
        # Categories of facts we want to extract
        fact_patterns = {
            "preference": [
                "i like", "i love", "i enjoy", "i prefer", "i'm fond of",
                "i don't like", "i hate", "i dislike"
            ],
            "habit": [
                "i usually", "i always", "i never", "i sometimes",
                "every day", "every week", "normally i"
            ],
            "personal_info": [
                "i am", "i'm", "my name is", "i work", "i live",
                "my job", "my home", "my family"
            ],
            "skill": [
                "i can", "i know how", "i'm good at", "i'm skilled in",
                "i'm experienced in", "i've learned"
            ],
            "goal": [
                "i want to", "i plan to", "i hope to", "i'm trying to",
                "my goal", "i aim to", "i wish to"
            ],
            "experience": [
                "i've been", "i have been", "i used to",
                "in my experience", "i remember when"
            ]
        }
        
        # Process user message
        lower_msg = user_message.lower()
        
        # Extract facts based on patterns
        for category, patterns in fact_patterns.items():
            for pattern in patterns:
                if pattern in lower_msg:
                    # Find the relevant sentence containing the pattern
                    sentences = user_message.split('.')
                    for sentence in sentences:
                        if pattern.lower() in sentence.lower():
                            facts.append({
                                "content": sentence.strip(),
                                "category": category,
                                "source": "user_message",
                                "confidence": "high" if pattern in ["i am", "i'm", "my name is"] else "medium",
                                "timestamp": datetime.now().isoformat()
                            })
        
        # Extract potential facts from assistant's response
        # Look for confirmations or clarifications
        lower_resp = assistant_response.lower()
        confirmation_patterns = [
            "you mentioned that", "you said", "as you told me",
            "based on what you said", "you indicated"
        ]
        
        for pattern in confirmation_patterns:
            if pattern in lower_resp:
                sentences = assistant_response.split('.')
                for sentence in sentences:
                    if pattern in sentence.lower():
                        facts.append({
                            "content": sentence.strip(),
                            "category": "confirmation",
                            "source": "assistant_response",
                            "confidence": "medium",
                            "timestamp": datetime.now().isoformat()
                        })
        
        return facts

    def add_fact(self, fact: Dict[str, str]) -> None:
        """Store an important fact about the user with metadata."""
        self.facts.add(
            documents=[fact["content"]],
            metadatas=[{
                "category": fact["category"],
                "source": fact["source"],
                "confidence": fact["confidence"],
                "timestamp": fact["timestamp"],
                "type": "fact"
            }],
            ids=[f"fact_{datetime.now().timestamp()}"]
        )

    def get_context_for_prompt(self, current_message: str) -> str:
        """Generate a context string from relevant memories."""
        memories = self.get_relevant_memories(current_message)
        
        # Organize facts by category
        categorized_facts = {}
        for fact in memories["facts"]:
            metadata = self.facts.get(where={"document": fact})
            if metadata and metadata["metadatas"]:
                category = metadata["metadatas"][0]["category"]
                if category not in categorized_facts:
                    categorized_facts[category] = []
                categorized_facts[category].append(fact)
        
        context_parts = []
        
        # Add categorized facts
        if categorized_facts:
            context_parts.append("What I know about you:")
            for category, facts in categorized_facts.items():
                context_parts.append(f"\n{category.title()}:")
                context_parts.extend(f"- {fact}" for fact in facts)
        
        # Add relevant conversations
        if memories["conversations"]:
            context_parts.append("\nRelevant past conversations:")
            context_parts.extend(f"- {conv}" for conv in memories["conversations"])
        
        return "\n".join(context_parts)