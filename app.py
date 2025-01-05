from fastapi import FastAPI, Request, Form, Cookie, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import json
from datetime import datetime
from storage import Storage
from conversation import ConversationHistory
from memory_manager import MemoryManager
from typing import Dict, List, Optional

app = FastAPI()

# Initialize components
templates = Jinja2Templates(directory="templates")
storage = Storage()
conversation_history = ConversationHistory()
memory_manager = MemoryManager()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

class ChatResponse(BaseModel):
    response: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("chat.html", {"request": request, "active_page": "chat"})

@app.get("/profile", response_class=HTMLResponse)
async def profile_form(request: Request) -> HTMLResponse:
    profile_data = storage.load_profile()
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "profile": profile_data,
        "active_page": "profile"
    })

@app.get("/memories", response_class=HTMLResponse)
async def view_memories(request: Request) -> HTMLResponse:
    facts = memory_manager.facts.get()
    conversations = memory_manager.conversations.get()
    
    categorized_facts: Dict[str, List[Dict]] = {}
    
    if facts["metadatas"]:
        for idx, metadata in enumerate(facts["metadatas"]):
            category = metadata.get("category", "uncategorized")
            if category not in categorized_facts:
                categorized_facts[category] = []
            
            categorized_facts[category].append({
                "content": facts["documents"][idx],
                "timestamp": metadata.get("timestamp", "Unknown"),
                "confidence": metadata.get("confidence", "medium")
            })
    
    recent_conversations = []
    if conversations["metadatas"]:
        for idx, metadata in enumerate(conversations["metadatas"]):
            recent_conversations.append({
                "content": conversations["documents"][idx],
                "timestamp": metadata.get("timestamp", "Unknown"),
                "session": metadata.get("session_id", "Unknown")
            })
    
    return templates.TemplateResponse(
        "memories.html",
        {
            "request": request,
            "facts": categorized_facts,
            "conversations": recent_conversations[-10:],  # Show last 10 conversations
            "active_page": "memories"
        }
    )

@app.post("/save_profile")
async def save_profile(
    request: Request,
    name: str = Form(...),
    birthdate: str = Form(...),
    location: str = Form(...),
    occupation: str = Form(...),
    interests: str = Form(...),
    goals: str = Form(...),
    preferences: str = Form(...)
) -> Dict:
    try:
        profile_data = {
            "name": name,
            "birthdate": birthdate,
            "location": location,
            "occupation": occupation,
            "interests": interests,
            "goals": goals,
            "preferences": preferences
        }
        
        storage.save_profile(profile_data)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/chat")
async def chat(
    message: str = Form(...),
    session: Optional[str] = Cookie(None),
    response: Response = None
) -> Dict:
    try:
        if not session:
            session = str(uuid.uuid4())
            response.set_cookie(key="session", value=session)
        
        profile_context = storage.get_context_for_prompt()
        conv_context = conversation_history.get_context_string(session)
        memory_context = memory_manager.get_context_for_prompt(message)
        
        full_prompt = f"""You are my personal AI assistant. Here's what I know about you:

{profile_context}

{conv_context}

{memory_context}

User message: {message}"""

        conversation_history.add_message(session, "user", message)
        
        llm_response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "codellama:7b-instruct",
                "prompt": full_prompt
            },
            stream=True
        )
        
        if llm_response.status_code == 200:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        resp_obj = json.loads(line.decode('utf-8'))
                        if resp_obj.get('response'):
                            full_response += resp_obj['response']
                    except json.JSONDecodeError:
                        continue
            
            if full_response:
                conversation_history.add_message(session, "assistant", full_response)
                memory_manager.add_conversation(session, message, full_response)
                
                facts = memory_manager.extract_facts_from_conversation(message, full_response)
                for fact in facts:
                    memory_manager.add_fact(fact)
                
                return {"response": full_response}
        
        return {"response": "Error: Unable to get response from LLM"}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}