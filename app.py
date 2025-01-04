from fastapi import FastAPI, Request, Form
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
async def chat(message: str = Form(...)):
    try:
        print(f"Received message: {message}")  # Debug print
        
        # Send request to Ollama
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   "model": "llama2",
                                   "prompt": message
                               },
                               stream=True)  # Enable streaming
        
        print(f"Ollama status code: {response.status_code}")  # Debug print
        
        # Parse the response
        if response.status_code == 200:
            # Ollama returns multiple JSON objects, one per line
            # Concatenate all responses to get the full message
            full_response = ""
            for line in response.text.strip().split('\n'):
                try:
                    resp_obj = json.loads(line)
                    if resp_obj.get('response'):
                        full_response += resp_obj['response']
                except json.JSONDecodeError:
                    continue
            
            if full_response:
                return {"response": full_response}
        
        return {"response": "Error: Unable to get response from LLM"}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}