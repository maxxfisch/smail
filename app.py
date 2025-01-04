from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import requests
import json

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates and storage
templates = Jinja2Templates(directory="templates")
storage = Storage()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

class ChatResponse(BaseModel):
    response: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def profile_form(request: Request):
    profile_data = storage.load_profile()
    return templates.TemplateResponse("profile.html", {"request": request, "profile": profile_data})

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
):
    profile_data = {
        "name": name,
        "birthdate": birthdate,
        "location": location,
        "occupation": occupation,
        "interests": interests,
        "goals": goals,
        "preferences": preferences,
        "last_updated": str(datetime.now())
    }
    
    storage.save_profile(profile_data)
    return {"success": True}

@app.post("/chat")
async def chat(message: str = Form(...)):
    try:
        print(f"Received message: {message}")  # Debug print
        
        # Get personal context
        context = storage.get_context_for_prompt()
        
        # Construct the full prompt
        full_prompt = f"""You are my personal AI assistant. Here's some context about me:

{context}

Please keep this context in mind when responding.

User message: {message}"""
        
        # Send request to Ollama
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   "model": "codellama:7b-instruct",
                                   "prompt": full_prompt
                               },
                               stream=True)  # Enable streaming
        
        print(f"Ollama status code: {response.status_code}")  # Debug print
        
        # Parse the response
        if response.status_code == 200:
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
            
            if full_response:
                return {"response": full_response}
        
        return {"response": "Error: Unable to get response from LLM"}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}