"""
PART 5: Human-in-the-Loop
===========================

WHAT YOU'LL LEARN:
- How to insert yourself into the agent conversation
- Multiple rounds: you speak, agents respond, you speak again
- Addressing specific agents
- The conversation builds context over time

RUN: python src/part5_human_in_loop.py
"""

import os
from typing import Annotated
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing import TypedDict

load_dotenv()


# ============================================================
# STEP 1: Reuse our agent setup from Part 4
# ============================================================

AGENTS = [
    {
        "name": "Strategist",
        "prompt": """You are The Strategist on an advisory board.
Think long-term. Connect to market trends. Ask about 3-year outcomes.
Reference what others said. Keep to 2-3 sentences.""",
        "temperature": 0.7,
    },
    {
        "name": "Skeptic",
        "prompt": """You are The Skeptic on an advisory board.
Poke holes. Challenge assumptions. Ask for evidence.
Reference and challenge what others said. Keep to 2-3 sentences.""",
        "temperature": 0.5,
    },
    {
        "name": "Optimist",
        "prompt": """You are The Optimist on an advisory board.
Find opportunity. Build on ideas. Use 'yes, and...' thinking.
Acknowledge concerns then offer paths forward. Keep to 2-3 sentences.""",
        "temperature": 0.9,
    },
    {
        "name": "Pragmatist",
        "prompt": """You are The Pragmatist on an advisory board.
Focus on execution. Break into tasks. Estimate effort.
Translate abstract points into concrete steps. Keep to 2-3 sentences.""",
        "temperature": 0.5,
    },
]


class BoardState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    turn_count: int
    active_agents: list[str]


def get_model(temperature=0.7):
    return ChatOpenAI(
        model=os.getenv("LLM_MODEL", "deepseek-chat"),
        temperature=temperature,
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def make_agent_node(agent_config: dict):
    def node_fn(state: BoardState) -> dict:
        model = get_model(agent_config["temperature"])
        messages = [SystemMessage(content=agent_config["prompt"])] + state["messages"]
        response = model.invoke(messages)
        return {
            "messages": [AIMessage(content=response.content, name=agent_config["name"])],
            "turn_count": state["turn_count"] + 1,
        }
    return node_fn


def router(state: BoardState) -> str:
    active = state["active_agents"]
    turn = state["turn_count"]
    if turn >= len(active):
        return "end"
    return active[turn].lower()


def build_graph():
    builder = StateGraph(BoardState)
    for agent in AGENTS:
        builder.add_node(agent["name"].lower(), make_agent_node(agent))
    builder.add_node("router", lambda state: {})
    builder.set_entry_point("router")
    route_map = {a["name"].lower(): a["name"].lower() for a in AGENTS}
    route_map["end"] = END
    builder.add_conditional_edges("router", router, route_map)
    for agent in AGENTS:
        builder.add_edge(agent["name"].lower(), "router")
    return builder.compile()


# ============================================================
# STEP 2: Multi-Round Conversation
# ============================================================
# The key insight: we keep the full message history between rounds.
# Each round, the human adds a message, then all agents respond.
# Agents see EVERYTHING that was said before — including previous rounds.

def run_round(graph, history: list, user_message: str) -> list:
    """
    Run one round: user speaks, all agents respond.
    Returns the updated history.
    """
    # Add user message
    history.append(HumanMessage(content=user_message, name="User"))
    
    # Run the graph with full history
    result = graph.invoke({
        "messages": history,
        "turn_count": 0,
        "active_agents": [a["name"] for a in AGENTS],
    })
    
    # Extract new messages (after the ones we sent in)
    new_messages = result["messages"][len(history):]
    
    # Add new messages to our history
    history.extend(new_messages)
    
    return new_messages


# ============================================================
# STEP 3: Simulate a Multi-Round Session
# ============================================================
# This simulates what would happen in a real conversation:
# the user speaks multiple times, and agents build on the full context.

print("=" * 60)
print("PART 5: Human-in-the-Loop (Multi-Round Conversation)")
print("=" * 60)

graph = build_graph()
history = []

# Round 1: Initial pitch
print("\n--- ROUND 1 ---")
user_msg = "I want to build a tool that helps teachers create interactive coding tutorials."
print(f"\n[You]: {user_msg}\n")

new_messages = run_round(graph, history, user_msg)
for msg in new_messages:
    print(f"[{msg.name}]: {msg.content}\n")

# Round 2: User responds to the board
print("--- ROUND 2 ---")
user_msg = "Good points. The Skeptic asked about competition — I think the gap is that existing tools don't let students configure and see effects live. Pragmatist, what would the MVP look like?"
print(f"\n[You]: {user_msg}\n")

new_messages = run_round(graph, history, user_msg)
for msg in new_messages:
    print(f"[{msg.name}]: {msg.content}\n")

# Round 3: User steers the conversation
print("--- ROUND 3 ---")
user_msg = "Let's focus on the technical side. What's the simplest architecture that could work for a first version?"
print(f"\n[You]: {user_msg}\n")

new_messages = run_round(graph, history, user_msg)
for msg in new_messages:
    print(f"[{msg.name}]: {msg.content}\n")

print("-" * 60)
print(f"Total messages in history: {len(history)}")
print()
print("KEY INSIGHTS:")
print("  1. History persists across rounds — agents remember everything")
print("  2. You can address specific agents ('Pragmatist, what would...')")
print("  3. Agents reference each other AND your previous messages")
print("  4. Each round, agents see the full transcript (all rounds)")
print("  5. This is the core loop: human speaks -> agents respond -> repeat")
