# Response Streaming Feature RFC

## Overview
This document outlines the technical implementation details for adding response streaming capabilities to the SMAIL chat application, as specified in the ResponseStreamingPRD.md.

## System Architecture

### Components
1. Backend (FastAPI)
   - SSE Endpoint for streaming
   - Cancellation Handler
   - Error Recovery System
   - State Management

2. Frontend (JavaScript)
   - Stream Consumer
   - UI State Manager
   - Animation Controller
   - Error Handler

3. Shared
   - Message Protocol
   - State Definitions
   - Error Types

## Detailed Design

### Backend Implementation

#### 1. SSE Endpoint
```python
@app.get("/stream")
async def stream_response(prompt: str):
    async def event_generator():
        try:
            async for chunk in llm.stream(prompt):
                yield {
                    "event": "message",
                    "data": {
                        "content": chunk.content,
                        "metadata": {
                            "token_count": len(chunk.content),
                            "is_code": chunk.is_code_block,
                            "is_link": chunk.is_link
                        }
                    }
                }
        except Exception as e:
            yield {
                "event": "error",
                "data": {"type": "llm_error", "message": str(e)}
            }

    return EventSourceResponse(event_generator())
```

#### 2. Cancellation Handler
```python
@app.post("/cancel")
async def cancel_stream(stream_id: str):
    if stream_id in active_streams:
        active_streams[stream_id].cancel()
        return {"status": "cancelled"}
    return {"status": "not_found"}
```

### Frontend Implementation

#### 1. Stream Consumer
```javascript
class StreamManager {
    constructor() {
        this.eventSource = null;
        this.buffer = [];
        this.displayInterval = null;
    }

    startStream(prompt) {
        this.eventSource = new EventSource(`/stream?prompt=${encodeURIComponent(prompt)}`);
        this.eventSource.onmessage = this.handleMessage.bind(this);
        this.eventSource.onerror = this.handleError.bind(this);
        this.startDisplayLoop();
    }

    handleMessage(event) {
        const data = JSON.parse(event.data);
        this.buffer.push(data);
    }

    startDisplayLoop() {
        const CHARS_PER_SECOND = 60;
        const INTERVAL = 1000 / CHARS_PER_SECOND;
        
        this.displayInterval = setInterval(() => {
            if (this.buffer.length > 0) {
                const chunk = this.buffer.shift();
                this.displayChunk(chunk);
            }
        }, INTERVAL);
    }
}
```

#### 2. UI State Manager
```javascript
class UIStateManager {
    constructor() {
        this.currentState = 'idle';
        this.messageQueue = [];
        this.currentMessageIndex = 0;
    }

    updateStatus(state) {
        this.currentState = state;
        this.updateStatusMessage();
        this.updateProgressBar();
        this.updateControls();
    }

    updateStatusMessage() {
        const messages = STATUS_MESSAGES[this.currentState];
        const message = messages[this.currentMessageIndex];
        
        document.getElementById('status').textContent = message;
        
        this.currentMessageIndex = (this.currentMessageIndex + 1) % messages.length;
    }
}
```

### Message Protocol

#### 1. Server-to-Client Messages
```typescript
interface StreamMessage {
    event: 'message' | 'error' | 'complete';
    data: {
        content?: string;
        metadata?: {
            token_count: number;
            is_code: boolean;
            is_link: boolean;
        };
        error?: {
            type: 'connection' | 'llm' | 'server';
            message: string;
            attempt?: number;
        };
    };
}
```

### Error Recovery

#### 1. Retry Logic
```javascript
class RetryManager {
    constructor(maxAttempts = 5, baseDelay = 5000) {
        this.maxAttempts = maxAttempts;
        this.baseDelay = baseDelay;
        this.attempts = 0;
    }

    async retry(operation) {
        while (this.attempts < this.maxAttempts) {
            try {
                return await operation();
            } catch (error) {
                this.attempts++;
                if (this.attempts >= this.maxAttempts) {
                    throw error;
                }
                const delay = this.calculateDelay();
                await this.wait(delay);
            }
        }
    }

    calculateDelay() {
        return this.baseDelay * Math.pow(2, this.attempts - 1);
    }
}
```

## Implementation Phases

### Phase 1: Core Streaming
1. Implement SSE endpoint
2. Basic stream consumption
3. Simple text display
4. Basic error handling

### Phase 2: UI Enhancement
1. Status messages
2. Progress bar
3. Cancellation button
4. Copy functionality

### Phase 3: Advanced Features
1. Code/link highlighting
2. Advanced error recovery
3. Animation refinements
4. Performance optimizations

## Testing Strategy

### Unit Tests
1. Stream message formatting
2. Error handling
3. Retry logic
4. UI state management

### Integration Tests
1. End-to-end streaming
2. Error recovery
3. Cancellation flow
4. UI state transitions

### Performance Tests
1. Message throughput
2. Animation smoothness
3. Memory usage
4. Error recovery timing

## Security Considerations
1. Rate limiting
2. Input validation
3. Error message sanitization
4. Resource cleanup

## Open Questions
1. Should we implement server-side buffering for slow clients?
2. How should we handle browser tab switching/background tabs?
3. What metrics should we collect for monitoring?

## Timeline
- Phase 1: 1 week
- Phase 2: 1 week
- Phase 3: 1 week
- Testing & Refinement: 1 week

Total estimated time: 4 weeks

## Migration Plan

### Phase 0: Preparation (1 day)
1. Add SSE Dependencies
   ```python
   from sse_starlette.sse import EventSourceResponse
   ```
2. Create new endpoint `/stream-chat` alongside existing `/chat`
3. Add feature flag `USE_STREAMING` to control rollout

### Phase 1: Basic Streaming (2 days)
1. Backend Changes
   ```python
   @app.get("/stream-chat")
   async def stream_chat(
       message: str,
       session: Optional[str] = Cookie(None),
       response_obj: Response = None
   ):
       # Reuse existing context building
       full_prompt = build_prompt(message, session)
       
       async def event_generator():
           try:
               async for chunk in llm.stream(full_prompt):
                   yield {
                       "event": "message",
                       "data": json.dumps({
                           "content": chunk.content
                       })
                   }
           except Exception as e:
               yield {
                   "event": "error",
                   "data": json.dumps({
                       "error": str(e)
                   })
               }
       
       return EventSourceResponse(event_generator())
   ```

2. Frontend Changes
   - Add StreamManager class alongside existing ChatManager
   - Implement basic character-by-character display
   - Add feature flag check in UI

### Phase 2: Enhanced UI (3 days)
1. Status Messages
   - Implement status message rotation system
   - Add loading animations
   - Update progress tracking

2. Error Handling
   - Add retry mechanism
   - Implement error state UI
   - Add reconnection logic

3. Response Controls
   - Add cancellation button
   - Implement copy functionality
   - Add progress bar

### Phase 3: Testing & Rollout (2 days)
1. Testing
   - Add unit tests for new endpoints
   - Test error scenarios
   - Performance testing

2. Gradual Rollout
   - Enable for 10% of sessions
   - Monitor error rates
   - Gather performance metrics

3. Full Migration
   - Switch feature flag to 100%
   - Deprecate old endpoint
   - Remove old code

### Phase 4: Cleanup & Optimization (2 days)
1. Code Cleanup
   - Remove feature flags
   - Clean up old tests
   - Update documentation

2. Performance Optimization
   - Optimize chunk sizes
   - Fine-tune animations
   - Cache improvements

## Rollback Plan
1. Immediate Rollback
   - Set `USE_STREAMING=false`
   - Revert to `/chat` endpoint
   - Clear session storage

2. Gradual Rollback
   - Identify affected sessions
   - Migrate data if needed
   - Monitor error rates

## Migration Risks
1. Performance Impact
   - Monitor memory usage
   - Watch for connection limits
   - Track response times

2. User Experience
   - Browser compatibility
   - Network conditions
   - UI responsiveness

3. Data Integrity
   - Message ordering
   - Partial responses
   - Session management

## Success Metrics
1. Technical Metrics
   - Response time < 100ms
   - Error rate < 1%
   - Memory usage stable

2. User Metrics
   - Reduced perceived latency
   - Decreased abandon rate
   - Increased engagement 