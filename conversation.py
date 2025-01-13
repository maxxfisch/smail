from typing import List, Dict, Any
from datetime import datetime

class ConversationHistory:
    def __init__(self, max_history: int = 10) -> None:
        self.max_history = max_history
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}

    def add_message(self, session_id: str, role: str, content: str) -> None:
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        message = {
            "role": role,
            "content": content,
            "timestamp": str(datetime.now())
        }
        
        self.conversations[session_id].append(message)
        
        if len(self.conversations[session_id]) > self.max_history:
            self.conversations[session_id] = self.conversations[session_id][-self.max_history:]

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        return self.conversations.get(session_id, [])

    def get_context_string(self, session_id: str, max_messages: int = 5) -> str:
        history = self.get_history(session_id)[-max_messages:]
        if not history:
            return ""
        
        context = ["Recent conversation:"]
        for msg in history:
            role = "You" if msg["role"] == "user" else "Assistant"
            context.append(f"{role}: {msg['content']}")
        
        return "\n".join(context)

    def get_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all messages for a session, with proper role mapping for display."""
        messages = self.get_history(session_id)
        return [
            {
                "role": "user" if msg["role"] == "user" else "bot",
                "content": msg["content"]
            }
            for msg in messages
        ]