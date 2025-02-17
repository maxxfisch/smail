# SMAIL Project Documentation

## Overview
SMAIL is a chat application that uses the llama3.2 language model through Ollama to provide intelligent responses. The application includes features like chat persistence, memory management, and user profiles.

## Current Status

### Core Features
- FastAPI-based web application
- Advanced chat interface with streaming responses
- Profile management system
- Sophisticated memory management for conversation context
- Chat persistence across sessions
- Uses llama3.2:latest model (2.0 GB) via Ollama
- Real-time response streaming with UI feedback
- Code and markdown formatting with syntax highlighting
- Comprehensive error handling and recovery
- Performance optimizations for long conversations

### Technical Details
- Model: llama3.2:latest
- Backend: FastAPI + Python
- Frontend: HTML + JavaScript (Class-based architecture)
- Storage: ChromaDB for memory, JSON for session data
- Session management: Cookie-based
- UI Libraries: Prism.js for syntax highlighting, Marked.js for markdown

### Recent Improvements
1. UI Enhancement & Controls
   - Status message rotation during processing
   - Enhanced typing indicators
   - Response controls (Cancel, Copy)
   - Progress tracking
   - Word count display
   - Feedback messages
   - Improved error state handling

2. Code/Link Highlighting
   - Syntax highlighting for multiple languages
   - Markdown formatting support
   - Automatic language detection
   - Clickable links with proper styling

3. Error Recovery
   - Automatic reconnection with exponential backoff
   - Clear error feedback
   - Retry functionality
   - Connection state management

4. Performance Optimization
   - Message caching system
   - Efficient DOM updates
   - Scroll performance improvements
   - Automatic cleanup of old messages
   - Memory management for long sessions

### Known Issues
- None currently tracked

### Testing Status
- Unit tests added for all core components
- Test coverage includes:
  - Storage operations
  - Memory management
  - Conversation history
  - Session handling
  - Chat functionality
  - Error recovery
  - Message formatting

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
   - Keep business logic in appropriate modules
   - Use templates for all HTML content
   - Maintain clear separation of concerns
   - Follow class-based architecture for frontend

## Future Plans

### Planned Features
1. Memory Management
   - Improve fact extraction accuracy
   - Add memory cleanup utilities
   - Implement advanced memory search
   - Add memory visualization

2. User Experience
   - Add conversation export
   - Add conversation tagging/categorization
   - Implement theme customization
   - Add keyboard shortcuts

3. Profile Improvements
   - Add profile preview
   - Visualize profile influence on responses
   - Add profile completeness indicators

### Technical Improvements
1. Testing
   - Add end-to-end tests
   - Implement CI/CD
   - Add performance benchmarks

2. Documentation
   - Add API documentation
   - Add setup instructions
   - Create user guide

3. Performance
   - Implement server-side caching
   - Optimize memory usage
   - Add response compression

## Common Issues and Solutions
1. Response Handling
   ```