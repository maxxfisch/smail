from typing import List, Dict
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            type TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_message(content: str, type: str) -> None:
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (content, type) VALUES (?, ?)', (content, type))
    conn.commit()
    conn.close()

def get_chat_history() -> List[Dict]:
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('SELECT content, type, timestamp FROM messages ORDER BY timestamp')
    messages = [
        {"content": content, "type": msg_type, "timestamp": ts}
        for content, msg_type, ts in c.fetchall()
    ]
    conn.close()
    return messages