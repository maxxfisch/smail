# Response Streaming Architecture Decision Record

## Status
Proposed

## Context
The current chat implementation lacks real-time feedback and visual responsiveness during response generation. We need to implement streaming responses with proper UI feedback while maintaining the existing functionality.

## Decision
Implement Server-Sent Events (SSE) based streaming with a layered architecture that separates concerns between streaming, state management, and UI updates.

## System Context (C4 Level 1)

![System Context Diagram](images/streaming_context.png)

<details>
<summary>PlantUML Source</summary>

```plantuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

LAYOUT_WITH_LEGEND()

title System Context diagram for Response Streaming

Person(user, "End User", "A user interacting with the chat interface")

System(smail, "SMAIL Chat System", "Provides streaming chat interface with real-time feedback")

System_Ext(ollama, "Ollama LLM", "Local LLM providing streaming responses")

Rel(user, smail, "Sends messages and views responses", "HTTP/SSE")
Rel(smail, ollama, "Streams prompts and receives responses", "HTTP/Streaming")
Rel_Back(smail, user, "Provides real-time feedback and responses", "SSE")
```
</details>

## Container (C4 Level 2)

![Container Diagram](images/streaming_container.png)

<details>
<summary>PlantUML Source</summary>

```plantuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_WITH_LEGEND()

title Container diagram for Response Streaming

Person(user, "End User", "A user interacting with the chat interface")

System_Boundary(smail, "SMAIL Chat System") {
    Container(web_ui, "Web Interface", "HTML, JavaScript", "Provides streaming chat UI with status updates and controls")
    
    Container(stream_manager, "Stream Manager", "JavaScript Class", "Handles SSE connection and message buffering")
    
    Container(ui_state, "UI State Manager", "JavaScript Class", "Manages UI states and animations")
    
    Container(backend_api, "Backend API", "FastAPI", "Provides streaming endpoints and handles LLM communication")
    
    Container(error_handler, "Error Handler", "Python/JavaScript", "Manages error recovery and retries")
    
    ContainerDb(session_store, "Session Store", "JSON", "Stores conversation history and state")
}

System_Ext(ollama, "Ollama LLM", "Provides streaming response generation")

Rel(user, web_ui, "Interacts with", "HTTPS")
Rel(web_ui, stream_manager, "Initiates streaming", "JavaScript")
Rel(stream_manager, ui_state, "Updates UI state", "JavaScript")
Rel(stream_manager, backend_api, "Connects to", "SSE")
Rel(backend_api, ollama, "Streams prompts", "HTTP")
Rel_Back(ollama, backend_api, "Returns chunks", "HTTP")
Rel(backend_api, session_store, "Stores/retrieves", "JSON")
Rel(error_handler, stream_manager, "Manages retries", "JavaScript")
Rel(error_handler, backend_api, "Handles errors", "HTTP")
```
</details>

## Consequences

### Positive
1. Real-time Feedback
   - Users see immediate response to their actions
   - Reduced perceived latency
   - More engaging interaction

2. Improved Error Handling
   - Graceful recovery from connection issues
   - Clear error feedback
   - Automatic retry mechanism

3. Better State Management
   - Clear separation of concerns
   - Predictable UI states
   - Easier debugging

### Negative
1. Increased Complexity
   - More moving parts
   - More state to manage
   - More error scenarios to handle

2. Browser Compatibility
   - SSE support required
   - Fallback mechanism needed
   - More testing required

3. Resource Usage
   - Long-lived connections
   - More memory usage
   - Higher server load

## Technical Details

### Components

1. Stream Manager
   - Handles SSE connection
   - Buffers incoming messages
   - Controls display timing
   - Manages retry logic

2. UI State Manager
   - Tracks current state
   - Updates status messages
   - Controls animations
   - Manages progress indicators

3. Backend API
   - Provides SSE endpoint
   - Handles LLM communication
   - Manages session state
   - Implements error recovery

4. Error Handler
   - Implements retry logic
   - Provides error feedback
   - Manages recovery flow
   - Tracks error metrics

### Data Flow

1. Request Flow
   ```
   User -> Web UI -> Stream Manager -> Backend API -> LLM
   ```

2. Response Flow
   ```
   LLM -> Backend API -> Stream Manager -> UI State Manager -> Web UI -> User
   ```

3. Error Flow
   ```
   Error -> Error Handler -> Stream Manager -> UI State Manager -> User
   ```

## Alternatives Considered

1. WebSocket Implementation
   - Pros: Full-duplex communication
   - Cons: Overkill for one-way streaming, more complex
   - Decision: Rejected as too complex for needs

2. Polling Implementation
   - Pros: Simple, widely compatible
   - Cons: Higher latency, more server load
   - Decision: Rejected due to poor user experience

3. Chunked HTTP Response
   - Pros: Simple implementation
   - Cons: Less control over streaming
   - Decision: Rejected due to limited control

## Implementation Strategy

1. Phase 1: Core Infrastructure
   - SSE endpoint
   - Basic streaming
   - Simple UI updates

2. Phase 2: Enhanced Features
   - Status messages
   - Progress tracking
   - Error handling

3. Phase 3: Polish
   - Animations
   - Performance optimization
   - Browser compatibility

## Monitoring and Metrics

1. Performance Metrics
   - Response time
   - Chunk delivery time
   - Memory usage
   - Connection count

2. Error Metrics
   - Error rates
   - Retry counts
   - Recovery success rate
   - Connection drops

3. User Metrics
   - Time to first chunk
   - Total response time
   - User engagement
   - Feature usage 