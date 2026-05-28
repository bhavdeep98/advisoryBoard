"""
PART 2: System Prompts & Personality
=====================================

WHAT YOU'LL LEARN:
- How system prompts shape behavior
- Same model, different personality = different agent
- Effect of temperature on output

RUN: python src/part2_system_prompts.py
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


# ============================================================
# STEP 1: Define Agent Personalities
# ============================================================
# An "agent" is just a model + a system prompt.
# The system prompt is the most powerful lever you have.
# Change it, and the same model behaves completely differently.

AGENTS = {
    "Strategist": {
        "prompt": """You are The Strategist. You think long-term and see the big picture.
You ask 'what does this look like in 3 years?' You connect ideas to trends.
Keep responses to 2-3 sentences.""",
        "temperature": 0.7,
    },
    "Skeptic": {
        "prompt": """You are The Skeptic. You poke holes in every idea.
You ask for evidence. You find risks others miss. You're blunt but constructive.
Keep responses to 2-3 sentences.""",
        "temperature": 0.5,
    },
    "Optimist": {
        "prompt": """You are The Optimist. You find opportunity everywhere.
You use 'yes, and...' thinking. You connect dots others miss. You're energetic.
Keep responses to 2-3 sentences.""",
        "temperature": 0.9,
    },
    "Pragmatist": {
        "prompt": """You are The Pragmatist. You focus on execution.
You ask 'what do we build Monday morning?' You estimate effort and find blockers.
Keep responses to 2-3 sentences.""",
        "temperature": 0.5,
    },
}


# ============================================================
# STEP 2: Same Question, Different Agents
# ============================================================
# Watch how the same question gets completely different answers
# depending on the system prompt.

def ask_agent(agent_name: str, question: str) -> str:
    """Send a question to a specific agent and return the response."""
    agent = AGENTS[agent_name]
    model = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "deepseek-chat"),
        temperature=agent["temperature"],
        base_url=os.getenv("OPENAI_BASE_URL"),
    )
    messages = [
        SystemMessage(content=agent["prompt"]),
        HumanMessage(content=question),
    ]
    response = model.invoke(messages)
    return response.content


question = "I want to build an AI-powered personal finance app."

print("=" * 60)
print("PART 2: Same Question, Four Different Agents")
print("=" * 60)
print(f"\nQuestion: {question}\n")
print("-" * 60)

for name in AGENTS:
    response = ask_agent(name, question)
    print(f"\n[{name}] (temp={AGENTS[name]['temperature']})")
    print(f"  {response}")

print()


# ============================================================
# STEP 3: Temperature Comparison
# ============================================================
# Temperature controls randomness:
#   0.0 = deterministic (same answer every time)
#   0.7 = balanced
#   2.0 = very creative/random
#
# Let's ask the same question 3 times at different temperatures.

print("=" * 60)
print("TEMPERATURE COMPARISON")
print("=" * 60)
print(f"\nSame question asked 3 times at each temperature level:")
print(f"Question: Give me a one-word name for a finance app.\n")

for temp in [0.0, 1.0, 2.0]:
    model = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "deepseek-chat"),
        temperature=temp,
        base_url=os.getenv("OPENAI_BASE_URL"),
    )
    messages = [
        SystemMessage(content="Respond with exactly one word."),
        HumanMessage(content="Give me a one-word name for a finance app."),
    ]
    
    results = []
    for _ in range(3):
        r = model.invoke(messages)
        results.append(r.content.strip())
    
    print(f"  temp={temp}: {results}")

print()
print("KEY INSIGHT: Low temperature = consistent. High temperature = varied.")
print("For advisory board agents, the Skeptic uses low temp (precise),")
print("the Optimist uses high temp (creative).")
