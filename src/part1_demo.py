"""
Part 1 Demo: Non-interactive test of the agent.
Runs a scripted conversation so you can see the agent in action.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

# Setup model
model = ChatOpenAI(
    model=os.getenv("LLM_MODEL", "deepseek-chat"),
    temperature=0.7,
    base_url=os.getenv("OPENAI_BASE_URL"),
)

print("=" * 60)
print("Part 1 Demo: Advisory Board Agent Test")
print("=" * 60)

# --- Demo 1: Basic conversation with memory ---
print("\n--- Demo 1: Basic conversation (shows memory works) ---\n")

messages = [SystemMessage(content="You are a helpful assistant. Keep answers to 2-3 sentences.")]

questions = [
    "What's the most important thing when starting a new project?",
    "Can you expand on your first point specifically?",  # Tests memory - references previous answer
    "Summarize what we've discussed so far.",  # Tests memory - should recall both turns
]

for q in questions:
    messages.append(HumanMessage(content=q))
    response = model.invoke(messages)
    messages.append(response)
    print(f"You: {q}")
    print(f"Agent: {response.content}\n")

# --- Demo 2: System prompt changes behavior ---
print("\n--- Demo 2: Same question, different personalities ---\n")

test_question = "Should I build a social media app?"

personalities = [
    ("Helpful Assistant", "You are a helpful assistant. Keep answers to 2-3 sentences."),
    ("Pessimist", "You are extremely pessimistic. Find the downside in everything. Keep answers to 2-3 sentences."),
    ("Pirate", "You are a pirate. Respond in pirate speak. Keep answers to 2-3 sentences."),
    ("5-year-old", "You are a 5-year-old explaining things to another 5-year-old. Keep answers to 2-3 sentences."),
]

for name, prompt in personalities:
    msgs = [SystemMessage(content=prompt), HumanMessage(content=test_question)]
    response = model.invoke(msgs)
    print(f"[{name}]: {response.content}\n")

print("=" * 60)
print("Demo complete! The same model, different system prompts = different agents.")
print("=" * 60)
