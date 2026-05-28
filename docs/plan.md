# Project Plan: Advisory Board Multi-Agent Chat

## Vision

A group chat interface where four AI agents with distinct personalities debate and collaborate on your ideas. Built step-by-step as a learning project using LangChain/LangGraph.

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  Chat UI (React)                 │
│         Messages with agent names/avatars        │
└─────────────────────┬───────────────────────────┘
                      │ WebSocket
┌─────────────────────▼───────────────────────────┐
│              FastAPI Backend                      │
│         Session management, streaming            │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│            LangGraph Orchestrator                 │
│    Turn-taking, state, human-in-the-loop         │
├─────────────────────────────────────────────────┤
│  Strategist  │  Skeptic  │  Optimist  │ Pragmatist│
│    Node      │   Node    │    Node    │   Node    │
└─────────────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│           LLM Provider (flexible)                │
│      OpenAI / Anthropic / Local / etc.           │
└─────────────────────────────────────────────────┘
```

## Agent Design

### The Strategist
- **System prompt focus:** Long-term thinking, market positioning, vision
- **Behavior:** Asks clarifying questions about goals, draws connections to trends, thinks in timelines
- **Trigger phrases:** "In 3 years...", "The bigger play here is...", "Positioning-wise..."

### The Skeptic
- **System prompt focus:** Risk identification, assumption testing, failure modes
- **Behavior:** Challenges claims, asks for evidence, identifies what could go wrong
- **Trigger phrases:** "Here's why this fails...", "What evidence do you have?", "The assumption here is..."

### The Optimist
- **System prompt focus:** Opportunity finding, creative connections, potential
- **Behavior:** Builds on ideas, finds adjacent opportunities, reframes negatives
- **Trigger phrases:** "Yes, and...", "What if we also...", "The opportunity here is..."

### The Pragmatist
- **System prompt focus:** Execution, feasibility, concrete next steps
- **Behavior:** Breaks things into tasks, estimates effort, identifies blockers
- **Trigger phrases:** "Concretely, Monday morning...", "The first step is...", "That's a 2-week project because..."

## Turn-Taking Logic

1. User sends a message
2. Orchestrator decides which agents respond (not always all four)
3. Agents respond in sequence, each seeing previous responses
4. Agents can reference and react to each other
5. User can interrupt, redirect, or address specific agents

## State Management

- Conversation history (all messages from all participants)
- Per-agent memory (what each agent has said and committed to)
- Topic tracking (what's being discussed, decisions made)
- User preferences (which agents they engage with most)

## Part-by-Part Breakdown

### Part 1: Single Agent (LangChain Basics)
- Install langchain, set up API keys
- Create a simple chat model call
- Add conversation memory
- Tutorial: what are chains, models, prompts

### Part 2: Agent with Personality
- System prompts that create distinct behavior
- Output parsing (structured vs freeform)
- Temperature and model parameter tuning
- Tutorial: prompt engineering for personality

### Part 3: Two Agents Talking (LangGraph Basics)
- Install langgraph
- Create a graph with two nodes (two agents)
- Pass state between them
- Simple back-and-forth conversation
- Tutorial: nodes, edges, state, graph execution

### Part 4: Four Agents Debating
- Expand to four agent nodes
- Turn-taking logic (who speaks when)
- Shared conversation state
- Agents referencing each other's points
- Tutorial: multi-agent orchestration patterns

### Part 5: Human-in-the-Loop
- Add user input as a graph node
- LangGraph interrupt/resume for user turns
- Addressing specific agents
- Steering the conversation
- Tutorial: human-in-the-loop patterns in LangGraph

### Part 6: Backend API
- FastAPI app with WebSocket endpoint
- Streaming agent responses token-by-token
- Session management (multiple conversations)
- Tutorial: FastAPI + WebSocket + async patterns

### Part 7: Chat UI
- React (or vanilla JS) chat interface
- Agent messages with distinct names/colors/avatars
- Real-time streaming display
- Conversation history
- Tutorial: WebSocket client, chat UI patterns

## File Structure (target)

```
advisory-board/
├── README.md
├── docs/
│   ├── plan.md
│   ├── part1-single-agent.md
│   ├── part2-personality.md
│   ├── part3-two-agents.md
│   ├── part4-advisory-board.md
│   ├── part5-human-in-loop.md
│   ├── part6-backend-api.md
│   └── part7-chat-ui.md
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── strategist.py
│   │   ├── skeptic.py
│   │   ├── optimist.py
│   │   └── pragmatist.py
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── orchestrator.py
│   │   └── state.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── websocket.py
│   └── config.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── requirements.txt
├── .env.example
└── .gitignore
```

## Decisions Made

- LangGraph over raw LangChain for multi-agent orchestration
- FastAPI + WebSocket for real-time communication
- Provider-flexible (not locked to OpenAI or Anthropic)
- Tutorial-first approach: each part teaches concepts, not just code
- Advisory board theme: Strategist, Skeptic, Optimist, Pragmatist
