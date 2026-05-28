# Advisory Board: Multi-Agent Tutorial

A step-by-step code tutorial for building a multi-agent AI system with LangChain and LangGraph. Each part is a self-contained Python script you can read, understand, and run.

Built for teachers and students who want to understand multi-agent systems by reading and running real code.

## The Concept

Four AI agents with distinct personalities debate your ideas:

| Agent | Role | Style |
|-------|------|-------|
| Strategist | Big picture, long-term | "What does this look like in 3 years?" |
| Skeptic | Pokes holes, stress-tests | "Here's why this fails..." |
| Optimist | Finds opportunity | "Yes, and what if we also..." |
| Pragmatist | Execution focus | "What do we build Monday?" |

## Tutorial Parts

Run each script in order. Each one builds on the concepts from the previous.

```bash
# Activate virtual environment first
.\venv\Scripts\activate   # Windows
source venv/bin/activate   # Mac/Linux

# Then run each part
python src/part1_chat_model.py
python src/part2_system_prompts.py
python src/part3_langgraph_basics.py
python src/part4_advisory_board.py
python src/part5_human_in_loop.py
```

| Part | File | What You Learn |
|------|------|----------------|
| 1 | `part1_chat_model.py` | Chat models, message types, conversation memory |
| 2 | `part2_system_prompts.py` | System prompts as personality, temperature effects |
| 3 | `part3_langgraph_basics.py` | LangGraph nodes, edges, state, two agents debating |
| 4 | `part4_advisory_board.py` | Four agents, round-robin, enable/disable agents |
| 5 | `part5_human_in_loop.py` | Multi-round conversation, addressing specific agents |

## Setup

```bash
# Clone
git clone https://github.com/bhavdeep98/advisoryBoard.git
cd advisoryBoard

# Virtual environment
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate   # Mac/Linux

# Install
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env — add your API key (OpenAI, DeepSeek, or any OpenAI-compatible provider)
```

## How to Read the Code

Each file follows the same structure:
1. **Header** — what you'll learn, how to run it
2. **Steps** — numbered sections with comments explaining every concept
3. **Output** — the script runs and prints results so you see it working
4. **Key Insights** — summary at the end of what to take away

The code IS the tutorial. Read it top to bottom.

## Tech Stack

- Python 3.10+
- LangChain (model abstraction)
- LangGraph (multi-agent orchestration)
- Any OpenAI-compatible LLM (DeepSeek, OpenAI, Anthropic, Ollama)

## License

MIT
