# Advisory Board Playground

An interactive teaching tool for multi-agent AI systems. Configure AI agents live and see how changes affect a group conversation in real-time.

Built step-by-step with LangChain/LangGraph as a learning project.

## What Is This?

A web app with two panels:
- **Left:** Agent configuration cards (system prompt, temperature, model, on/off toggle)
- **Right:** Live group chat where agents debate your ideas

Change a setting, see the effect immediately. Built for teachers and students who want to understand how multi-agent systems work by experimenting with them.

## The Agents

| Agent | Role | Personality |
|-------|------|-------------|
| The Strategist | Big picture, long-term thinking | "What does this look like in 3 years?" |
| The Skeptic | Pokes holes, stress-tests | "Here's why this fails..." |
| The Optimist | Finds opportunity, builds on ideas | "Yes, and what if we also..." |
| The Pragmatist | Execution focus, next steps | "Ok but what do we build Monday?" |

All configurable. Change their personality, swap their role, disable them, crank up the randomness.

## Teaching Presets

- **Default Advisory Board** — balanced team, good starting point
- **Echo Chamber** — all agents agree (shows why diversity matters)
- **Maximum Chaos** — high temperature, contradictory prompts
- **Minimal** — one agent, bare prompt (starting point for students)

## Tech Stack

- **Python + LangGraph** — agent orchestration, state, turn-taking
- **FastAPI** — backend API + WebSocket for real-time
- **HTML/CSS/JS** — simple frontend, no framework dependency
- **LLM Flexible** — OpenAI, Anthropic, or any LangChain-supported provider

## Learning Path (7 Parts)

Each part is a standalone tutorial with working code and a "demo moment" you can show in class.

| Part | What You Build | Key Learning |
|------|---------------|--------------|
| 1 | Single agent in terminal | LangChain basics: models, prompts, memory |
| 2 | Configurable personality | System prompts, temperature effects |
| 3 | Two agents talking | LangGraph: nodes, edges, state |
| 4 | Four agents debating | Multi-agent orchestration, turn-taking |
| 5 | Human-in-the-loop | Interrupts, user input, conversation steering |
| 6 | Backend + simple UI | FastAPI, WebSocket, streaming responses |
| 7 | Configuration playground | Live config editing, presets, teaching UI |

## Getting Started

See `docs/` for tutorials. Start with [Part 1: Single Agent](docs/part1-single-agent.md).

## Setup

```bash
# Clone and enter
git clone <this-repo>
cd advisory-board

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Copy env and add your API key
cp .env.example .env
# Edit .env with your OpenAI or Anthropic key
```

## License

MIT
