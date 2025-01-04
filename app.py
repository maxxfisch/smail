from fastapi import FastAPI, Request, Form
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
async def chat(message: str = Form(...)):
    try:
        print(f"Received message: {message}")  # Debug print
        
        # Send request to Ollama
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   "model": "codellama:7b-instruct",
                                   "prompt": message
                               },
                               stream=True)  # Enable streaming
        
        print(f"Ollama status code: {response.status_code}")  # Debug print
        
        # Parse the response
        if response.status_code == 200:
            # Ollama returns multiple JSON objects, one per line
            # Concatenate all responses to get the full message
            full_response = ""
            
            # Read the response line by line
            for line in response.iter_lines():
                if line:
                    try:
                        resp_obj = json.loads(line.decode('utf-8'))
                        print(f"Response object: {resp_obj}")  # Debug print
                        if resp_obj.get('response'):
                            full_response += resp_obj['response']
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error: {e}")  # Debug print
                        continue
            
            print(f"Full response: {full_response}")  # Debug print
            
            if full_response:
                return {"response": full_response}
            else:
                print("No response content accumulated")  # Debug print
        
        return {"response": "Error: Unable to get response from LLM"}
    except Exception as e:
        print(f"Exception occurred: {str(e)}")  # Debug print
        return {"response": f"Error: {str(e)}"}