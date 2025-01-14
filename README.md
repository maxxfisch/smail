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
graph TB
    User["End User<br/><sub>Person using web browser</sub>"]
    SMAIL["SMAIL Application<br/><sub>Web-based chat interface</sub>"]
    Ollama["Ollama LLM<br/><sub>Local AI service</sub>"]
    
    subgraph Local["Local Environment"]
        SMAIL
        Ollama
    end
    
    User -->|"Uses web interface<br/>HTTPS"| SMAIL
    SMAIL -->|"Sends prompts<br/>HTTP/JSON"| Ollama
    Ollama -->|"Returns responses<br/>HTTP/JSON"| SMAIL
```

### Container Diagram (C4 Level 2)
```mermaid
graph TB
    User["End User<br/><sub>Person using chat interface</sub>"]
    
    subgraph Local["Local Environment"]
        subgraph SMAIL["SMAIL Application"]
            WebUI["Web Interface<br/><sub>HTML + JavaScript<br/>Class-based components</sub>"]
            Backend["Backend Service<br/><sub>Python + FastAPI<br/>Business logic & sessions</sub>"]
            Storage["Data Storage<br/><sub>JSON + ChromaDB<br/>Profiles & memories</sub>"]
        end
        
        Ollama["Ollama LLM<br/><sub>Local AI service</sub>"]
    end
    
    User -->|"Interacts with<br/>HTTPS"| WebUI
    WebUI -->|"Makes API calls<br/>REST API"| Backend
    Backend -->|"Returns responses<br/>REST API"| WebUI
    Backend -->|"Persists data<br/>Local FS"| Storage
    Backend -->|"Sends prompts<br/>HTTP/JSON"| Ollama
    Ollama -->|"Returns responses<br/>HTTP/JSON"| Backend
```

### Components
- Frontend: HTML/JavaScript with class-based state management
- Backend: FastAPI (Python) with persistent storage
- LLM: Ollama (local) with llama2 model
- Storage: JSON-based persistence for conversations and profiles
- Memory: ChromaDB for vector storage and fact extraction
