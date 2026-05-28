"""
PART 1: Your First Chat Model
===============================

WHAT YOU'LL LEARN:
- What a chat model is
- How to call it with LangChain
- The three message types (System, Human, AI)

RUN: python src/part1_chat_model.py
"""

# ============================================================
# STEP 1: Setup
# ============================================================
# We load API keys from a .env file so they're not in our code.
# python-dotenv reads .env and puts values into os.environ.

import os
from dotenv import load_dotenv

load_dotenv()  # Reads .env file in the project root


# ============================================================
# STEP 2: Create a Chat Model
# ============================================================
# A chat model is the simplest building block in LangChain.
# It's a function: takes messages in, returns a message out.
#
# We use ChatOpenAI which works with any OpenAI-compatible API
# (OpenAI, DeepSeek, Ollama, etc.) by setting the base_url.

from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model=os.getenv("LLM_MODEL", "deepseek-chat"),  # Which model to use
    temperature=0.7,                                  # 0=deterministic, 2=random
    base_url=os.getenv("OPENAI_BASE_URL"),           # API endpoint (None=OpenAI default)
)


# ============================================================
# STEP 3: Message Types
# ============================================================
# LangChain uses three message types:
#
#   SystemMessage  - Instructions for the AI (personality, rules)
#   HumanMessage   - What the user says
#   AIMessage      - What the AI responded (used for history)
#
# You send a LIST of messages. The model reads them all and
# generates the next response.

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


# ============================================================
# STEP 4: Make a Simple Call
# ============================================================
# The most basic operation: send messages, get a response.

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is LangChain in one sentence?"),
]

response = model.invoke(messages)

print("=" * 60)
print("PART 1: Basic Chat Model Call")
print("=" * 60)
print()
print(f"Question: What is LangChain in one sentence?")
print(f"Response: {response.content}")
print()


# ============================================================
# STEP 5: Conversation with Memory
# ============================================================
# "Memory" is just keeping a list of all messages and sending
# the full list each time. The model doesn't actually remember
# anything — you're giving it the full transcript.

print("-" * 60)
print("CONVERSATION WITH MEMORY:")
print("-" * 60)
print()

# Start fresh with a system prompt
history = [SystemMessage(content="You are a helpful assistant. Keep answers brief.")]

# Turn 1
history.append(HumanMessage(content="My name is Alex."))
response = model.invoke(history)
history.append(response)  # Store the response for next turn
print(f"Human: My name is Alex.")
print(f"AI:    {response.content}")
print()

# Turn 2 — the model "remembers" because we send the full history
history.append(HumanMessage(content="What's my name?"))
response = model.invoke(history)
history.append(response)
print(f"Human: What's my name?")
print(f"AI:    {response.content}")
print()

# Show what we're actually sending
print("-" * 60)
print("WHAT'S ACTUALLY BEING SENT (the full message list):")
print("-" * 60)
for i, msg in enumerate(history):
    role = type(msg).__name__.replace("Message", "")
    print(f"  [{i}] {role}: {msg.content[:80]}")
print()
print("KEY INSIGHT: The model sees ALL messages every time.")
print("That's why it 'remembers' — we're sending the full transcript.")
