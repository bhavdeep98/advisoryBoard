# Advisory Board Multi-Agent Chat

A web chat app where you pitch ideas to a panel of four AI advisors. They debate each other, respond to you, and you can steer the conversation. Like a group chat with opinionated experts.

## The Agents

| Agent | Role | Personality |
|-------|------|-------------|
| The Strategist | Big picture, market positioning, long-term thinking | Calm, structured, asks "what does this look like in 3 years?" |
| The Skeptic | Pokes holes, finds risks, stress-tests assumptions | Blunt, contrarian, "here's why this fails" |
| The Optimist | Finds opportunity, builds on ideas, sees potential | Energetic, "yes and..." mentality, connects dots |
| The Pragmatist | Execution focus, feasibility, next concrete step | Grounded, "ok but what do we actually build Monday?" |

## How It Works

1. You type a message (an idea, a question, a decision)
2. Agents take turns responding, reacting to you AND each other
3. They can agree, disagree, build on each other's points
4. You can address specific agents, ask follow-ups, or redirect
5. Conversation state persists so context builds over time

## Tech Stack

- **Python + LangGraph** — agent orchestration, state management, turn-taking
- **FastAPI** — backend API + WebSocket for real-time chat
- **React or HTML/JS** — chat UI with agent names/avatars
- **LLM Provider Flexible** — OpenAI, Anthropic, etc. via LangChain model abstraction

## Learning Path (7 Parts)

Each part is a standalone tutorial with working code. Part N always works before you start Part N+1.

| Part | What You Build | What You Learn |
|------|---------------|----------------|
| 1 | Single agent in a terminal | LangChain basics: models, prompts, chains, memory |
| 2 | Agent with a personality | System prompts, prompt engineering, output parsing |
| 3 | Two agents talking to each other | LangGraph basics: nodes, edges, state, graph execution |
| 4 | Four agents debating (advisory board) | Multi-agent orchestration, turn-taking logic, shared state |
| 5 | Human-in-the-loop | LangGraph interrupts, user input nodes, conversation steering |
| 6 | Backend API | FastAPI + WebSocket, streaming responses, session management |
| 7 | Chat UI | Frontend that shows agent messages with names/avatars, real-time updates |

## Getting Started

See `docs/` for tutorials. Start with [Part 1: Single Agent](docs/part1-single-agent.md).
