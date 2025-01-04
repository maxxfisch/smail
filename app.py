from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import json

app = FastAPI()

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