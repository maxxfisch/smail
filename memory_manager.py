import chromadb
from chromadb.config import Settings
import os
from datetime import datetime
from typing import List, Dict, Any

class MemoryManager:
    def __init__(self, data_dir: str = "data") -> None:
        self.data_dir = data_dir
        self.memory_dir = os.path.join(data_dir, "memory")
        os.makedirs(self.memory_dir, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=self.memory_dir)
        self.conversations = self.client.get_or_create_collection("conversations")
        self.facts = self.client.get_or_create_collection("facts")

    def add_conversation(self, session_id: str, user_message: str, assistant_response: str) -> None:
        full_exchange = f"User: {user_message}\nAssistant: {assistant_response}"
        self.conversations.add(
            documents=[full_exchange],
            metadatas=[{
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "type": "conversation"
            }],
            ids=[f"conv_{datetime.now().timestamp()}"]
        )

    def add_fact(self, fact: Dict[str, str]) -> None:
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

    def get_relevant_memories(self, query: str, limit: int = 5) -> Dict[str, List[str]]:
        conv_results = self.conversations.query(query_texts=[query], n_results=limit)
        fact_results = self.facts.query(query_texts=[query], n_results=limit)
        
        return {
            "conversations": conv_results["documents"][0] if conv_results["documents"] else [],
            "facts": fact_results["documents"][0] if fact_results["documents"] else []
        }

    def extract_facts_from_conversation(self, user_message: str, assistant_response: str) -> List[Dict[str, str]]:
        facts = []
        fact_patterns = {
            "preference": ["i like", "i love", "i enjoy", "i prefer", "i'm fond of", "i don't like", "i hate", "i dislike"],
            "habit": ["i usually", "i always", "i never", "i sometimes", "every day", "every week", "normally i"],
            "personal_info": ["i am", "i'm", "my name is", "i work", "i live", "my job", "my home", "my family"],
            "skill": ["i can", "i know how", "i'm good at", "i'm skilled in", "i'm experienced in", "i've learned"],
            "goal": ["i want to", "i plan to", "i hope to", "i'm trying to", "my goal", "i aim to", "i wish to"],
            "experience": ["i've been", "i have been", "i used to", "in my experience", "i remember when"]
        }
        
        lower_msg = user_message.lower()
        for category, patterns in fact_patterns.items():
            for pattern in patterns:
                if pattern in lower_msg:
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
        
        confirmation_patterns = ["you mentioned that", "you said", "as you told me", "based on what you said", "you indicated"]
        lower_resp = assistant_response.lower()
        
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

    def get_context_for_prompt(self, current_message: str) -> str:
        memories = self.get_relevant_memories(current_message, limit=3)  # Reduced from 5 to 3
        context_parts = []
        
        relevant_facts = []
        for fact in memories["facts"]:
            metadata = self.facts.get(where={"document": fact})
            if metadata and metadata["metadatas"]:
                confidence = metadata["metadatas"][0].get("confidence", "medium")
                if confidence == "high":
                    relevant_facts.append(fact)
        
        if relevant_facts:
            context_parts.extend(relevant_facts)
        
        if memories["conversations"]:
            most_relevant = memories["conversations"][0]
            if most_relevant and len(most_relevant.strip()) > 0:
                context_parts.append(most_relevant)
        
        return "\n".join(context_parts) if context_parts else ""