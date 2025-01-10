# SMAIL Project Documentation

## Overview
SMAIL is a chat application that uses the llama3.2 language model through Ollama to provide intelligent responses. The application includes features like chat persistence, memory management, and user profiles.

## Current Status

### Core Features
- FastAPI-based web application
- Chat interface with streaming responses
- Profile management system
- Memory management for conversation context
- Chat persistence across sessions
- Uses llama3.2:latest model (2.0 GB) via Ollama

### Technical Details
- Model: llama3.2:latest
- Backend: FastAPI + Python
- Frontend: HTML + JavaScript
- Storage: File-based (JSON)
- Session management: Cookie-based

### Recent Fixes
- Fixed response handling in chat endpoint
- Corrected variable naming (response_obj vs response)
- Added proper imports (pydantic, uuid)
- Removed duplicate imports
- Fixed streaming response handling

### Known Issues
- None currently tracked

## Project Structure
```
smail/
├── app.py              # Main FastAPI application
├── conversation.py     # Conversation history management
├── memory_manager.py   # Long-term memory and fact extraction
├── storage.py         # File-based storage operations
└── templates/         # HTML templates
    ├── chat.html     # Main chat interface
    ├── memories.html # Memory viewing interface
    ├── nav.html     # Navigation component
    └── profile.html # Profile management interface
```

## Development Guidelines
1. Variable Naming:
   - Use `response_obj` for FastAPI Response objects
   - Use `llm_response` for Ollama API responses
   - Be consistent with naming across the application

2. Model Configuration:
   - Use the `MODEL_NAME` constant for model references
   - Current model: llama3.2:latest

3. Code Organization:
   - Keep business logic in appropriate modules (conversation.py, memory_manager.py, storage.py)
   - Use templates for all HTML content
   - Maintain clear separation of concerns

## Future Plans

### Planned Features
1. Response Streaming Improvements
   - Implement proper streaming UI feedback
   - Add typing indicators

2. Memory Management
   - Improve fact extraction
   - Add memory cleanup utilities
   - Implement memory search

3. User Experience
   - Add conversation export
   - Improve error handling and user feedback
   - Add conversation tagging/categorization

### Technical Improvements
1. Testing
   - Add unit tests
   - Add integration tests
   - Implement CI/CD

2. Documentation
   - Add API documentation
   - Improve code comments
   - Add setup instructions

3. Performance
   - Optimize memory usage
   - Add caching where appropriate
   - Improve response times

## Common Issues and Solutions
1. Response Handling
   ```python
   # Correct way to handle responses
   llm_response = requests.post(
       OLLAMA_URL,
       json={"model": MODEL_NAME, "prompt": prompt},
       stream=True
   )
   ```

2. FastAPI Response Objects
   ```python
   # Correct parameter naming
   async def endpoint(response_obj: Response):
       response_obj.set_cookie(...)
   ```

3. Model Usage
   ```python
   # Use constants for model configuration
   MODEL_NAME = "llama3.2:latest"
   ```

## Contributing
1. Create feature branches for new work
2. Maintain consistent code style
3. Test changes thoroughly
4. Document new features or changes
5. Create detailed pull requests

## Deployment
Currently running locally with:
```bash
uvicorn app:app --reload
```

Requirements:
- Python 3.x
- Ollama with llama3.2:latest model
- FastAPI and dependencies from requirements.txt