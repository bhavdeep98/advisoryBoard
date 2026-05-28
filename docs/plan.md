# Project Plan: Advisory Board Playground

## Vision

An interactive teaching tool where users configure AI agents and immediately see how those changes affect a live group conversation. Built step-by-step as a learning project using LangChain/LangGraph.

**Primary audience:** Students and developers learning about multi-agent systems.
**Core interaction:** Tweak agent configuration (personality, temperature, model) → see the effect in real-time conversation.

## Teaching Goals

- Demystify how system prompts shape agent behavior
- Show the effect of temperature, model choice, and prompt wording
- Let people experiment with multi-agent dynamics (enable/disable agents, change roles)
- Provide a sandbox where "breaking things" is encouraged

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                        Web UI (Playground)                        │
├────────────────────────────┬─────────────────────────────────────┤
│   Config Panel (left)      │      Conversation Panel (right)     │
│                            │                                     │
│  ┌──────────────────────┐  │  ┌─────────────────────────────┐   │
│  │ Agent Card: Strategist│  │  │ [Strategist] In 3 years...  │   │
│  │ - System prompt [edit]│  │  │ [Skeptic] Here's the risk...│   │
│  │ - Temperature [slider]│  │  │ [You] What about X?         │   │
│  │ - Model [dropdown]    │  │  │ [Optimist] Yes, and also... │   │
│  │ - Enabled [toggle]    │  │  └─────────────────────────────┘   │
│  └──────────────────────┘  │                                     │
│  ┌──────────────────────┐  │  ┌─────────────────────────────┐   │
│  │ Agent Card: Skeptic   │  │  │ [Type your message...]       │   │
│  │ ...                   │  │  └─────────────────────────────┘   │
│  └──────────────────────┘  │                                     │
└────────────────────────────┴─────────────────────────────────────┘
                      │ WebSocket
┌─────────────────────▼───────────────────────────┐
│              FastAPI Backend                      │
│     Session management, config hot-reload        │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│            LangGraph Orchestrator                 │
│    Turn-taking, state, human-in-the-loop         │
│    Config-driven (agents rebuild on change)       │
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

## Interactive Teaching Features

### Live Configuration
- Edit any agent's system prompt mid-conversation and see behavior shift
- Temperature slider (0.0 to 2.0) with real-time effect
- Model selector per agent (compare GPT-4o vs Claude vs smaller models)
- Toggle agents on/off to see how group dynamics change

### "What Changed?" Indicators
- When config changes, next response is highlighted
- Side-by-side comparison: "before" vs "after" a config change
- Tooltip explanations: "Temperature 0.2 = more predictable, 1.5 = more creative"

### Presets for Teaching
- "Default Advisory Board" — balanced team
- "Echo Chamber" — all agents agree (shows why diversity matters)
- "Maximum Chaos" — high temperature, contradictory prompts
- "Minimal" — one agent, bare system prompt (starting point for students)

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
- **Demo moment:** Change the system prompt, re-run, see different behavior
- Tutorial: what are chains, models, prompts

### Part 2: Agent with Personality (Configurable)
- System prompts that create distinct behavior
- Temperature and model parameter tuning
- **Demo moment:** Same question, different temperature — show the output spread
- **Teaching hook:** "What makes an agent feel like a character vs a generic bot?"
- Tutorial: prompt engineering for personality

### Part 3: Two Agents Talking (LangGraph Basics)
- Install langgraph
- Create a graph with two nodes (two agents)
- Pass state between them
- Simple back-and-forth conversation
- **Demo moment:** Change one agent's prompt, watch the conversation shift
- Tutorial: nodes, edges, state, graph execution

### Part 4: Four Agents Debating (Advisory Board)
- Expand to four agent nodes
- Turn-taking logic (who speaks when)
- Shared conversation state
- Agents referencing each other's points
- **Demo moment:** Disable the Skeptic — watch the group become an echo chamber
- Tutorial: multi-agent orchestration patterns

### Part 5: Human-in-the-Loop
- Add user input as a graph node
- LangGraph interrupt/resume for user turns
- Addressing specific agents
- Steering the conversation
- **Demo moment:** Redirect the conversation mid-debate, see agents adapt
- Tutorial: human-in-the-loop patterns in LangGraph

### Part 6: Backend API + Simple UI
- FastAPI app with WebSocket endpoint
- Streaming agent responses token-by-token
- Simple HTML/CSS/JS chat interface (no React dependency)
- Agent messages with distinct names/colors
- **Demo moment:** Open in browser, type a message, see agents respond live
- Tutorial: FastAPI + WebSocket + frontend basics

### Part 7: Configuration Playground (Full Teaching UI)
- Config panel: editable system prompts, temperature sliders, model selectors, toggles
- Live hot-reload: change config mid-conversation without restarting
- Presets: "Default", "Echo Chamber", "Maximum Chaos", "Minimal"
- "What changed?" highlights on responses after config edits
- **Demo moment:** Live demo in class — students change settings and see effects
- Tutorial: building interactive teaching tools, state management

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
