# SMAIL - Simple Machine Learning Interface

A simple web interface for interacting with a local LLM using Ollama.

## Prerequisites

- Python 3.8 or higher
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
- The chat history is maintained in the browser session

## Architecture

- Frontend: HTML/JavaScript
- Backend: FastAPI (Python)
- LLM: Ollama (local) with llama2 model