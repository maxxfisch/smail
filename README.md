# SMAIL - Simple Machine Learning Interface

A simple web interface for interacting with a local LLM using Ollama.

## Prerequisites

- Python 3.8 or higher (required for both installation and runtime)
- Ollama installed and running locally
- A compatible LLM model (default: llama2)

## Setup

1. Install Ollama following instructions at [Ollama's website](https://ollama.ai/)

2. Pull the llama2 model:
```bash
ollama pull llama2
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn app:app --reload
```

5. Open your browser and navigate to `http://localhost:8000`

## Usage

- Type your message in the input field and press Enter or click Send
- The LLM will process your message and respond
- Chat history persists between page navigations and browser sessions
- Use the Profile page to customize your experience
- Visit the Memories page to view conversation history and extracted facts

## Architecture

### System Context (C4 Level 1)
```mermaid
C4Context
    title SMAIL System Context - High Level View

    Person(user, "End User", "Person interacting with the AI assistant through their web browser")
    
    Boundary(local, "Local Environment") {
        System(smail, "SMAIL Application", "Web-based chat interface with memory management and profile customization")
        System_Ext(ollama, "Ollama LLM", "Local language model service (llama2)")
    }
    
    Rel(user, smail, "Uses web interface", "HTTPS")
    Rel(smail, ollama, "Sends prompts", "HTTP/JSON")
    Rel(ollama, smail, "Returns responses", "HTTP/JSON")
```

### Container Diagram (C4 Level 2)
```mermaid
C4Container
    title SMAIL Container Architecture - Detailed View

    Person(user, "End User", "Person using the chat interface")
    
    Boundary(local, "Local Environment") {
        Boundary(smail, "SMAIL Application") {
            Container(web_ui, "Web Interface", "HTML + JavaScript", "Class-based components with persistent state management and real-time chat")
            Container(web_app, "Backend Service", "Python + FastAPI", "RESTful API handling sessions, business logic, and component coordination")
            ContainerDb(storage, "Data Storage", "JSON + ChromaDB", "Profile data, conversation history, and vector-based semantic memory")
        }
        
        System_Ext(ollama, "Ollama LLM", "Local AI model service")
    }
    
    Rel(user, web_ui, "Interacts with", "HTTPS")
    Rel(web_ui, web_app, "Makes API calls", "REST API")
    Rel(web_app, web_ui, "Returns responses", "REST API")
    Rel(web_app, storage, "Persists data", "Local FS")
    Rel(web_app, ollama, "Sends prompts", "HTTP/JSON")
    Rel(ollama, web_app, "Returns responses", "HTTP/JSON")
```

### Components
- Frontend: HTML/JavaScript with class-based state management
- Backend: FastAPI (Python) with persistent storage
- LLM: Ollama (local) with llama2 model
- Storage: JSON-based persistence for conversations and profiles
- Memory: ChromaDB for vector storage and fact extraction
