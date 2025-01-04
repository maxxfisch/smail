from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import json
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

class ChatResponse(BaseModel):
    response: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
async def chat(message: str):
    try:
        # Send request to Ollama
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   "model": "llama2",
                                   "prompt": message
                               })
        
        # Parse the response
        if response.status_code == 200:
            # Ollama returns multiple JSON objects, one per line
            last_response = None
            for line in response.text.strip().split('\n'):
                last_response = json.loads(line)
            
            if last_response and 'response' in last_response:
                return {"response": last_response['response']}
        
        return {"response": last_response['response']}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from Ollama")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)