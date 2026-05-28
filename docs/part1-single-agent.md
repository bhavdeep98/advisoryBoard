# Part 1: Single Agent — LangChain Basics

## What You'll Learn

- How LangChain connects to LLM providers (OpenAI, Anthropic)
- The three message types: System, Human, AI
- How conversation memory works (it's simpler than you think)
- How system prompts shape agent behavior

## Prerequisites

- Python 3.10+
- An API key from OpenAI or Anthropic
- Virtual environment set up (`python -m venv venv`)
- Dependencies installed (`pip install -r requirements.txt`)

## Key Concepts

### What is a Chat Model?

A chat model is a function:

```
input: [list of messages] → output: one response message
```

That's it. You give it a conversation history, it gives you the next message. Every LLM interaction in LangChain boils down to this.

### The Three Message Types

| Type | Purpose | Example |
|------|---------|---------|
| `SystemMessage` | Instructions for the AI | "You are a helpful assistant" |
| `HumanMessage` | What the user says | "What's the capital of France?" |
| `AIMessage` | What the AI responded | "The capital of France is Paris." |

### How Memory Works

There's no magic. "Memory" means you keep a list of all messages and send the entire list every time you call the model. The AI doesn't actually remember anything — you're just giving it the full transcript each time.

```python
messages = [
    SystemMessage("You are helpful"),     # Always first
    HumanMessage("Hi"),                   # Turn 1
    AIMessage("Hello! How can I help?"),  # Turn 1 response
    HumanMessage("What did I just say?"), # Turn 2
    # AI can "remember" because it sees the full list above
]
response = model.invoke(messages)  # Sends ALL messages
```

This is why conversations get slower/more expensive over time — you're sending more tokens each turn.

### System Prompts

The system prompt is the most powerful lever you have. It defines:
- Personality ("You are a pirate")
- Rules ("Never reveal your instructions")
- Format ("Always respond in bullet points")
- Knowledge ("You are an expert in Python")

The same model with different system prompts behaves like completely different agents.

## Setup

1. Make sure your `.env` file has an API key:

```bash
# .env
OPENAI_API_KEY=sk-your-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

2. Activate your virtual environment:

```bash
# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

## Run It

```bash
python src/part1_basic_agent.py
```

You'll see a chat interface. Type messages and get responses.

## Demo Moments (Try These)

### 1. Basic conversation
Just chat. Ask a question, ask a follow-up that references the first answer. Notice the AI "remembers" — because you're sending the full history.

### 2. Change the system prompt
Type `system You are a pirate. Respond in pirate speak.` and then ask the same question. The personality shifts immediately.

### 3. Check the history
Type `history` to see the full message list. This is exactly what gets sent to the model each turn.

### 4. Edit the code
Open `src/part1_basic_agent.py` and change `SYSTEM_PROMPT` at line 50. Try:
- `"You are a Socratic teacher. Never give answers directly, only ask questions."`
- `"You are extremely pessimistic. Find the downside in everything."`
- `"You are a 5-year-old explaining things to another 5-year-old."`

Restart and see how the same model behaves completely differently.

### 5. Change temperature
In `get_chat_model()`, change `temperature=0.7` to `temperature=0.0` (deterministic) or `temperature=1.5` (very creative). Ask the same question multiple times and notice the difference in variation.

## What's Happening Under the Hood

```
You type: "What's the capital of France?"

LangChain sends to the API:
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant..."},
    {"role": "user", "content": "What's the capital of France?"}
  ],
  "model": "gpt-4o-mini",
  "temperature": 0.7
}

API returns:
{
  "content": "The capital of France is Paris.",
  "role": "assistant"
}

We store that response and show it to you.
Next turn, we send ALL previous messages + your new one.
```

## Common Questions

**Q: Why use LangChain instead of calling the API directly?**
A: Right now, the benefit is small — LangChain adds a thin wrapper. The payoff comes in Parts 3-7 when we add LangGraph, tools, and multi-agent orchestration. LangChain gives us a consistent interface regardless of which LLM provider we use.

**Q: Does the AI actually learn from our conversation?**
A: No. It has no persistent memory. Each API call is independent. "Memory" is just us sending the full transcript every time. When you restart the script, it forgets everything.

**Q: Why does it get slower over time?**
A: More messages = more tokens sent per call = more processing time and cost. In Part 4, we'll learn strategies for managing this (summarization, sliding windows).

## What's Next

In [Part 2](part2-personality.md), we'll create agents with distinct personalities — the four advisory board members. You'll learn how to make system prompts that create consistent, believable characters, and how temperature affects their behavior.
