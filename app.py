from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import json

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
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
        
        return {"response": "Error: Unable to get response from LLM"}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}