from fastapi import FastAPI, Request, Form, Cookie, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import requests
import json
from datetime import datetime
from storage import Storage
from conversation import ConversationHistory

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates, storage, and conversation history
templates = Jinja2Templates(directory="templates")
storage = Storage()
conversation_history = ConversationHistory()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

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
    try:
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
    except Exception as e:
        print(f"Error saving profile: {str(e)}")  # Debug print
        return {"success": False, "error": str(e)}

@app.post("/chat")
async def chat(
    message: str = Form(...),
    session: str = Cookie(None),
    response: Response = None
):
    try:
        # Create or get session ID
        if not session:
            session = str(uuid.uuid4())
            response.set_cookie(key="session", value=session)

        print(f"Received message: {message}")  # Debug print
        
        # Get personal context and conversation history
        context = storage.get_context_for_prompt()
        conv_context = conversation_history.get_context_string(session)
        
        # Construct the full prompt
        full_prompt = f"""You are my personal AI assistant. Here's some context about me:

{context}

{conv_context}

Please keep this context in mind when responding.

User message: {message}"""

        # Add user message to history
        conversation_history.add_message(session, "user", message)
        
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
                # Add assistant's response to history
                conversation_history.add_message(session, "assistant", full_response)
                return {"response": full_response}
        
        return {"response": "Error: Unable to get response from LLM"}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}