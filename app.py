#!/usr/bin/env python3

from typing import Dict, Optional, List
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import requests
import json
from pydantic import BaseModel
import uvicorn
from database import init_db, add_message, get_chat_history

app = FastAPI()
templates = Jinja2Templates(directory="templates")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

class ChatResponse(BaseModel):
    response: str

class Message(BaseModel):
    content: str
    type: str
    timestamp: str

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/chat/history")
async def get_history() -> List[Message]:
    return get_chat_history()

@app.post("/chat", response_model=ChatResponse)
async def chat(message: str) -> Dict[str, str]:
    if not message or message.isspace():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Store user message
    add_message(message, "user")

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": message},
            timeout=30
        )
        response.raise_for_status()
    except requests.ConnectionError:
        raise HTTPException(status_code=503, detail="Ollama service is not available")
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Request to Ollama timed out")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Ollama: {str(e)}")

    try:
        last_response: Optional[Dict] = None
        for line in response.text.strip().split('\n'):
            last_response = json.loads(line)
        
        if not last_response or 'response' not in last_response:
            raise HTTPException(status_code=500, detail="Invalid response from Ollama")
        
        # Store bot response
        bot_response = last_response['response']
        add_message(bot_response, "bot")
        
        return {"response": bot_response}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from Ollama")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)