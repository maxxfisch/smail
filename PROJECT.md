# SMAIL Project Documentation

## Overview
SMAIL is a chat application that uses the deepseek-r1:7b language model through Ollama to provide intelligent responses. The application includes features like chat persistence, memory management, and user profiles.

## Current Status

### Core Features
- FastAPI-based web application
- Advanced chat interface with streaming responses
- Profile management system
- Sophisticated memory management for conversation context
- Chat persistence across sessions
- Uses deepseek-r1:7b model (7.0 GB) via Ollama
- Real-time response streaming with UI feedback
- Code and markdown formatting with syntax highlighting
- Comprehensive error handling and recovery
- Performance optimizations for long conversations

### Technical Details
- Model: deepseek-r1:7b
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
   - Current model: deepseek-r1:7b

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

4. External Integrations
   - Internet Search Integration
     - Real-time web search capabilities
     - Source citation and attribution
     - Search result summarization
     - Safe browsing implementation

   - Slack Integration
     - Direct message support
     - Channel monitoring and responses
     - Thread-aware conversations
     - Slack command integration

   - Gmail Integration
     - Email composition assistance
     - Smart email summarization
     - Draft management
     - Email context awareness

5. Bullet Journal System
   - Digital Bullet Journal Implementation
     - Daily logs with rapid logging
     - Monthly and future logs
     - Collections and indexes
     - Migration capabilities
   - Smart Task Management
     - Bullet syntax (•, -, o, x) support
     - Task state tracking and updates
     - Automatic task migration
     - Priority signifiers
   - Journal Analytics
     - Task completion tracking
     - Habit monitoring
     - Productivity insights
     - Time management analysis
   - Custom Collections
     - Project trackers
     - Reading logs
     - Habit trackers
     - Meeting notes templates
   - AI-Enhanced Features
     - Smart task categorization
     - Pattern recognition in habits
     - Automated index generation
     - Context-aware task suggestions

6. Investment Portfolio Management
   - Portfolio Tracking
     - Real-time asset monitoring
     - Multi-currency support
     - Cryptocurrency integration
     - Custom portfolio grouping
   - Investment Analysis
     - Performance metrics and ROI
     - Risk assessment
     - Diversification analysis
     - Tax lot tracking
   - Market Intelligence
     - News sentiment analysis
     - Market trend detection
     - Correlation analysis
     - Economic indicator tracking
   - Trading Support
     - Trade journal and history
     - Strategy backtesting
     - Position sizing calculator
     - Risk management tools
   - AI-Powered Insights
     - Portfolio optimization suggestions
     - Market anomaly detection
     - Pattern recognition in trades
     - Personalized risk alerts

7. Health Management System
   - Health Metrics Tracking
     - Vital signs monitoring
     - Sleep patterns
     - Exercise and activity logs
     - Nutrition tracking
   - Medical Management
     - Medication schedules
     - Appointment tracking
     - Symptom journal
     - Medical history organization
   - Wellness Analytics
     - Health trend analysis
     - Correlation detection
     - Progress visualization
     - Habit impact assessment
   - Lifestyle Optimization
     - Exercise recommendations
     - Meal planning assistance
     - Stress management tools
     - Work-life balance tracking
   - AI Health Insights
     - Early warning detection
     - Lifestyle optimization suggestions
     - Health pattern recognition
     - Preventive care recommendations

8. Web Interaction System
   - Visual Understanding
     - Screen content analysis
     - UI element detection
     - Dynamic content tracking
     - Visual hierarchy understanding
   - Action Automation
     - Form filling
     - Navigation assistance
     - Click and type simulation
     - Workflow automation
   - Context Awareness
     - Page state tracking
     - Session management
     - Error detection
     - Dynamic content handling
   - Security Features
     - Credential management
     - Permission handling
     - Secure data transfer
     - Activity logging
   - AI-Enhanced Capabilities
     - Task understanding
     - Context-aware actions
     - Error recovery
     - Adaptive automation

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