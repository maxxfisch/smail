from fastapi import FastAPI, Request, Form, Cookie, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import requests
import json
import uuid
from datetime import datetime
from storage import Storage
from conversation import ConversationHistory
from memory_manager import MemoryManager

app = FastAPI()

# Initialize components
templates = Jinja2Templates(directory="templates")
storage = Storage()
conversation_history = ConversationHistory()
memory_manager = MemoryManager()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
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
        
        # Get all available context
        profile_context = storage.get_context_for_prompt()
        conv_context = conversation_history.get_context_string(session)
        memory_context = memory_manager.get_context_for_prompt(message)
        
        # Construct the full prompt
        full_prompt = f"""You are my personal AI assistant. Here's what I know about you:

Profile Information:
{profile_context}

Recent Conversation:
{conv_context}

Relevant Memories:
{memory_context}

Please use this context to provide a personalized response.

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
                # Add assistant's response to history
                conversation_history.add_message(session, "assistant", full_response)
                
                # Store conversation in long-term memory
                memory_manager.add_conversation(session, message, full_response)
                
                # Extract and store any facts from the conversation
                facts = memory_manager.extract_facts_from_conversation(message, full_response)
                for fact in facts:
                    memory_manager.add_fact(fact, "conversation")
                
                return {"response": full_response}
            else:
                print("No response content accumulated")  # Debug print
        
        return {"response": "Error: Unable to get response from LLM"}
    except Exception as e:
        print(f"Exception occurred: {str(e)}")  # Debug print
        return {"response": f"Error: {str(e)}"}