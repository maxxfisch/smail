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
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

LAYOUT_WITH_LEGEND()

title System Context diagram for SMAIL

Person(user, "End User", "Person using web browser to interact with the AI assistant")

Boundary(local, "Local Environment") {
    System(smail, "SMAIL Application", "Web-based chat interface with memory management and profile customization")
    System_Ext(ollama, "Ollama LLM", "Local language model service running llama2")
}

Rel(user, smail, "Uses web interface", "HTTPS")
Rel(smail, ollama, "Sends prompts", "HTTP/JSON")
Rel_Back(smail, ollama, "Returns responses", "HTTP/JSON")
@enduml
```

### Container Diagram (C4 Level 2)
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_WITH_LEGEND()

title Container diagram for SMAIL

Person(user, "End User", "Person using the chat interface")

Boundary(local, "Local Environment") {
    System_Boundary(smail, "SMAIL Application") {
        Container(web_ui, "Web Interface", "HTML, JavaScript", "Class-based components with persistent state management and real-time chat")
        Container(web_app, "Backend Service", "Python, FastAPI", "RESTful API handling sessions, business logic, and component coordination")
        ContainerDb(storage, "Data Storage", "JSON, ChromaDB", "Profile data, conversation history, and vector-based semantic memory")
    }
    
    System_Ext(ollama, "Ollama LLM", "Local AI model service")
}

Rel(user, web_ui, "Interacts with", "HTTPS")
Rel(web_ui, web_app, "Makes API calls", "REST API")
Rel_Back(web_ui, web_app, "Returns responses", "REST API")
Rel(web_app, storage, "Reads/writes data", "Local FS")
Rel(web_app, ollama, "Sends prompts", "HTTP/JSON")
Rel_Back(web_app, ollama, "Returns responses", "HTTP/JSON")
@enduml
```

### Components
- Frontend: HTML/JavaScript with class-based state management
- Backend: FastAPI (Python) with persistent storage
- LLM: Ollama (local) with llama2 model
- Storage: JSON-based persistence for conversations and profiles
- Memory: ChromaDB for vector storage and fact extraction
