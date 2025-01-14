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
    title SMAIL System Context
    
    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")

    Person_Ext(user, "End User", "A person seeking to interact with an AI assistant through a web interface")
    
    System(smail, "SMAIL Application", "A web-based interface that provides intelligent chat, memory management, and personalized interactions through local LLM integration")
    
    System_Ext(ollama, "Ollama LLM Service", "Local large language model service running llama2, providing AI capabilities without cloud dependencies")
    
    UpdateRelStyle(user, smail, $textColor="green", $lineColor="green")
    Rel(user, smail, "Interacts with", "HTTPS (Browser)")
    
    UpdateRelStyle(smail, ollama, $textColor="blue", $lineColor="blue")
    BiRel(smail, ollama, "Sends prompts to and receives responses from", "HTTP/JSON")
```

### Container Diagram (C4 Level 2)
```mermaid
C4Container
    title SMAIL Container Diagram
    
    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")

    Person_Ext(user, "End User", "A person seeking to interact with an AI assistant")
    
    System_Boundary(smail, "SMAIL Application") {
        Container(web_ui, "Web Interface", "HTML, JavaScript, Class-based Components", "Provides responsive user interface with persistent state management and real-time chat functionality")
        
        Container(web_app, "Backend API", "Python, FastAPI", "Handles HTTP requests, manages business logic, session handling, and coordinates between components")
        
        ContainerDb(storage, "Storage Layer", "JSON Files, ChromaDB Vector Store", "Manages persistent storage of profiles, conversations, and semantic memory with vector embeddings")
    }
    
    System_Ext(ollama, "Ollama LLM", "Local LLM service providing AI capabilities")
    
    UpdateRelStyle(user, web_ui, $textColor="green", $lineColor="green")
    Rel(user, web_ui, "Uses", "HTTPS")
    
    UpdateRelStyle(web_ui, web_app, $textColor="blue", $lineColor="blue")
    BiRel(web_ui, web_app, "Exchanges data via", "HTTP/JSON")
    
    UpdateRelStyle(web_app, storage, $textColor="red", $lineColor="red")
    Rel(web_app, storage, "Reads from and writes to", "Local File System")
    
    UpdateRelStyle(web_app, ollama, $textColor="purple", $lineColor="purple")
    BiRel(web_app, ollama, "Exchanges prompts and responses", "HTTP/JSON")
```

### Components
- Frontend: HTML/JavaScript with class-based state management
- Backend: FastAPI (Python) with persistent storage
- LLM: Ollama (local) with llama2 model
- Storage: JSON-based persistence for conversations and profiles
- Memory: ChromaDB for vector storage and fact extraction
