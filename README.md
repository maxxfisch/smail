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
    title System Context Diagram for SMAIL
    
    Person(user, "User", "A person who wants to chat with an AI assistant")
    
    System(smail, "SMAIL", "Simple Machine Learning Interface that provides chat, memory, and profile management")
    
    System_Ext(ollama, "Ollama", "Local LLM service running llama2 model")
    
    Rel(user, smail, "Uses", "HTTP")
    Rel(smail, ollama, "Sends prompts to", "HTTP")
    Rel(ollama, smail, "Returns responses", "HTTP")
    Rel(smail, user, "Displays responses to", "HTTP")
```

### Container Diagram (C4 Level 2)
```mermaid
C4Container
    title Container Diagram for SMAIL
    
    Person(user, "User", "A person who wants to chat with an AI assistant")
    
    System_Boundary(smail, "SMAIL") {
        Container(web_app, "Web Application", "FastAPI + Python", "Handles HTTP requests, manages state and business logic")
        Container(web_ui, "Web Interface", "HTML + JavaScript", "Provides user interface and chat functionality")
        ContainerDb(file_store, "File Storage", "JSON + ChromaDB", "Stores profiles, conversations, and vector embeddings")
    }
    
    System_Ext(ollama, "Ollama", "Local LLM service")
    
    Rel(user, web_ui, "Interacts with", "HTTPS")
    Rel(web_ui, web_app, "Makes API calls to", "HTTP")
    Rel(web_app, file_store, "Reads from and writes to")
    Rel(web_app, ollama, "Sends prompts to", "HTTP")
    Rel(ollama, web_app, "Returns responses", "HTTP")
    Rel(web_app, web_ui, "Sends data to", "HTTP/WebSocket")
```

### Components
- Frontend: HTML/JavaScript with class-based state management
- Backend: FastAPI (Python) with persistent storage
- LLM: Ollama (local) with llama2 model
- Storage: JSON-based persistence for conversations and profiles
- Memory: ChromaDB for vector storage and fact extraction
