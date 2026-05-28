"""
PART 3: LangGraph Basics — Two Agents Talking
===============================================

WHAT YOU'LL LEARN:
- What LangGraph is and why we need it
- Nodes, edges, and state
- How to make two agents have a conversation

RUN: python src/part3_langgraph_basics.py

WHY LANGGRAPH?
LangChain handles single model calls. But when you want multiple
agents taking turns, sharing state, and making decisions about
who speaks next — that's orchestration. LangGraph is built for this.

Think of it as a flowchart:
  - Nodes = things that happen (agent responds, router decides)
  - Edges = connections between nodes (what happens next)
  - State = shared data that flows through the graph
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
# STEP 1: Define the State
# ============================================================
# State is the shared memory that all nodes can read and write.
# Here, it's just the conversation messages.
#
# `add_messages` is a "reducer" — it means new messages get
# APPENDED to the list, not replaced.

class ConversationState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    turn_count: int


# ============================================================
# STEP 2: Create Agent Nodes
# ============================================================
# Each node is a function that:
#   1. Reads the current state
#   2. Does something (calls the model)
#   3. Returns updates to the state

def get_model(temperature=0.7):
    return ChatOpenAI(
        model=os.getenv("LLM_MODEL", "deepseek-chat"),
        temperature=temperature,
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


STRATEGIST_PROMPT = """You are The Strategist in a two-person debate.
You think long-term, see the big picture, and ask about 3-year outcomes.
Respond to what the other person said. Keep it to 2-3 sentences.
Address the Skeptic directly when responding to their points."""

SKEPTIC_PROMPT = """You are The Skeptic in a two-person debate.
You poke holes, challenge assumptions, and ask for evidence.
Respond to what the other person said. Keep it to 2-3 sentences.
Address the Strategist directly when responding to their points."""


def strategist_node(state: ConversationState) -> dict:
    """The Strategist thinks and responds."""
    model = get_model(temperature=0.7)
    messages = [SystemMessage(content=STRATEGIST_PROMPT)] + state["messages"]
    response = model.invoke(messages)
    return {
        "messages": [AIMessage(content=response.content, name="Strategist")],
        "turn_count": state["turn_count"] + 1,
    }


def skeptic_node(state: ConversationState) -> dict:
    """The Skeptic challenges and responds."""
    model = get_model(temperature=0.5)
    messages = [SystemMessage(content=SKEPTIC_PROMPT)] + state["messages"]
    response = model.invoke(messages)
    return {
        "messages": [AIMessage(content=response.content, name="Skeptic")],
        "turn_count": state["turn_count"] + 1,
    }


# ============================================================
# STEP 3: Define the Router
# ============================================================
# The router decides what happens next.
# After each agent speaks, should the other respond? Or stop?

def should_continue(state: ConversationState) -> str:
    """Decide: keep debating or stop?"""
    if state["turn_count"] >= 4:  # 2 turns each
        return "end"
    # Alternate: Strategist -> Skeptic -> Strategist -> Skeptic
    if state["turn_count"] % 2 == 0:
        return "strategist"
    else:
        return "skeptic"


# ============================================================
# STEP 4: Build the Graph
# ============================================================
# Connect the nodes with edges.
#
# Graph structure:
#   START -> router -> strategist -> router -> skeptic -> router -> ... -> END

builder = StateGraph(ConversationState)

# Add nodes
builder.add_node("strategist", strategist_node)
builder.add_node("skeptic", skeptic_node)

# Add a router node that just passes through
def router_node(state: ConversationState) -> dict:
    return {}

builder.add_node("router", router_node)

# Entry point
builder.set_entry_point("router")

# Router decides who goes next
builder.add_conditional_edges(
    "router",
    should_continue,
    {
        "strategist": "strategist",
        "skeptic": "skeptic",
        "end": END,
    }
)

# After each agent speaks, go back to router
builder.add_edge("strategist", "router")
builder.add_edge("skeptic", "router")

# Compile the graph
graph = builder.compile()


# ============================================================
# STEP 5: Run It
# ============================================================
# Give the agents a topic and watch them debate.

topic = "We should build an AI-powered personal finance app."

print("=" * 60)
print("PART 3: Two Agents Debating via LangGraph")
print("=" * 60)
print(f"\nTopic: {topic}")
print(f"Format: Strategist and Skeptic take 2 turns each.")
print("-" * 60)

# Initial state: the human's message starts the debate
initial_state = {
    "messages": [HumanMessage(content=topic, name="User")],
    "turn_count": 0,
}

# Run the graph
result = graph.invoke(initial_state)

# Print the debate
print()
for msg in result["messages"]:
    if hasattr(msg, "name") and msg.name:
        speaker = msg.name
    elif isinstance(msg, HumanMessage):
        speaker = "User"
    else:
        speaker = "Unknown"
    print(f"[{speaker}]: {msg.content}\n")

print("-" * 60)
print("KEY INSIGHTS:")
print("  1. Each agent is a node (a function that reads state and returns updates)")
print("  2. The router decides who speaks next (conditional edges)")
print("  3. State (messages) flows through the graph — agents see each other's words")
print("  4. The graph stops when should_continue returns 'end'")
