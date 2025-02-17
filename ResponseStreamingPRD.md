# Response Streaming Feature PRD

## Overview
This document outlines the requirements for implementing proper response streaming in the SMAIL chat application, including UI feedback and typing indicators.

## Problem Statement
Currently, the chat interface lacks proper visual feedback during response generation, which can lead to uncertainty about whether the system is processing the request or not.

## Goals
- Improve user experience by providing real-time feedback
- Make the chat interaction feel more natural and responsive
- Reduce perceived latency during response generation
- Add personality to the interface through engaging status messages

## Non-Goals
- Implementing full real-time chat capabilities
- Adding multi-user chat features
- Modifying the underlying LLM response generation

## User Stories
1. As a user, I want to see when the AI is "thinking" about my message
2. As a user, I want to see the response being typed out in real-time
3. As a user, I want to know if there's an error during response generation
4. As a user, I want to be able to cancel a response if it's not what I'm looking for
5. As a user, I want to see engaging status messages that make the interaction more enjoyable

## Functional Requirements

### Response Generation States
1. Thinking State
   - Show a rotating set of playful status messages (round-robin rotation):
     - Initial Messages:
       - "🤔 Pondering the mysteries of your question..."
       - "🧠 Neural networks firing..."
       - "💭 Deep in thought..."
     - Processing Messages:
       - "📚 Flipping through my digital library..."
       - "🔍 Searching the knowledge base..."
       - "🎯 Getting to the heart of the matter..."
     - Response Messages:
       - "✍️ Crafting the perfect response..."
       - "🎨 Painting with words..."
       - "📝 Getting my thoughts together..."
   - Rotate messages every 3 seconds
   - Include a subtle loading animation
   - Display duration of current processing

2. Response Streaming
   - Show text appearing character by character at a consistent speed (60 chars/second)
   - Include a subtle cursor animation
   - Display word count/estimated time remaining
   - No variable typing speed simulation
   - Highlight special content during streaming:
     - Code blocks with syntax highlighting
     - Clickable links with distinct styling

3. Error States
   - Connection Loss: 
     - Primary: "📡 Oops, lost in space! Attempting reconnection (Attempt X/5)..."
     - Success: "🌟 We're back online! Regenerating response..."
     - Final Failure: "🔌 Connection lost. Please try again."
   - LLM Error: 
     - Primary: "🤯 Brain overload! Retrying (Attempt X/5)..."
     - Final Failure: "⚠️ Unable to generate response. Please rephrase your question."
   - Server Error: 
     - Primary: "🔧 Technical hiccup! Retrying (Attempt X/5)..."
     - Final Failure: "⚙️ Server issues. Please try again later."
   - Retry UI:
     - Show countdown timer during 5-second delay
     - Display "Retrying in: X seconds"
     - Include "Retry Now" button to skip countdown
     - Animate countdown progress

### Response Control
1. Cancellation
   - Add a prominent "Cancel" button during response generation
   - Show cancellation confirmation: "🛑 Response cancelled. What else can I help you with?"
   - Ensure clean state reset after cancellation

2. Partial Response Management
   - Enable copying of partial responses during streaming
   - Add a "Copy" button that becomes active as soon as content starts streaming
   - Maintain proper formatting when copying (including code blocks and links)

### UI Components
1. Status Bar
   - Location: Bottom of chat panel
   - Components:
     - Status message
     - Progress indicator showing response completion percentage
     - Cancel button (when applicable)
     - Word count/time estimate
     - Retry controls (when applicable)
       - Countdown timer
       - "Retry Now" button
       - Attempt counter (X/5)

2. Response Area
   - Typing indicator with cursor animation
   - Clear visual distinction between complete and in-progress responses
   - Smooth transition between states
   - Progress bar showing overall response completion
     - Subtle, non-intrusive design
     - Updates in real-time with streamed content
     - Color indicates current state (normal/error)

## Technical Requirements

### Backend Changes
1. Streaming Implementation
   - Use Server-Sent Events (SSE) for real-time updates
   - Implement proper error handling and recovery
   - Add cancellation endpoint

### Frontend Changes
1. State Management
   - Track response generation state
   - Handle connection interruptions
   - Manage animation states

2. Error Handling
   - Implement automatic reconnection
   - Provide clear error feedback
   - Save partial responses when possible

## Implementation Notes
1. Typing Speed
   - Fixed rate: 60 characters per second
   - No artificial variation
   - Consistent across all response types
   - Buffer next chunks while displaying current text

2. Status Message Rotation
   - Implement as a circular queue for each state
   - 3-second display time per message
   - Smooth transition animation between messages
   - State-specific message sets

3. Error Handling Implementation
   - Use exponential backoff with 5-second base
   - Maintain retry counter in session
   - Clear counter on successful response
   - Implement server-side retry tracking
   - Retry UI Components:
     - Circular progress indicator for countdown
     - Clickable "Retry Now" button
     - Attempt counter with clear visual feedback

4. Progress Tracking
   - Calculate progress based on token count from LLM
   - Update progress bar smoothly (avoid jumps)
   - Handle unknown total length gracefully
   - Use subtle animation for indeterminate progress 