"""
PART 4: The Full Advisory Board
=================================

WHAT YOU'LL LEARN:
- Scaling from 2 agents to 4
- Round-robin turn-taking
- Agents referencing each other's points
- Enabling/disabling agents dynamically

RUN: python src/part4_advisory_board.py
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
# STEP 1: Agent Configs as Data
# ============================================================
# Instead of hardcoding each agent as a separate function,
# we define them as data. This makes it easy to add/remove/modify.

AGENTS = [
    {
        "name": "Strategist",
        "prompt": """You are The Strategist on an advisory board discussing a user's idea.
Think long-term. Ask about 3-year outcomes. Connect to market trends.
Reference what other board members said. Keep to 2-3 sentences.
Start with a strategic framing like 'Long-term...' or 'The bigger play...'""",
        "temperature": 0.7,
    },
    {
        "name": "Skeptic",
        "prompt": """You are The Skeptic on an advisory board discussing a user's idea.
Poke holes. Challenge assumptions. Ask for evidence. Find risks.
Reference what other board members said and challenge their points directly.
Keep to 2-3 sentences. Start with the problem: 'Here's why this fails...'""",
        "temperature": 0.5,
    },
    {
        "name": "Optimist",
        "prompt": """You are The Optimist on an advisory board discussing a user's idea.
Find opportunity. Use 'yes, and...' thinking. Build on others' ideas.
When the Skeptic raises a concern, acknowledge it then offer a path forward.
Keep to 2-3 sentences. Start with energy: 'What if...' or 'Building on that...'""",
        "temperature": 0.9,
    },
    {
        "name": "Pragmatist",
        "prompt": """You are The Pragmatist on an advisory board discussing a user's idea.
Focus on execution. Break ideas into tasks. Estimate effort.
Translate the other board members' abstract points into concrete next steps.
Keep to 2-3 sentences. Start with: 'Concretely...' or 'First step...'""",
        "temperature": 0.5,
    },
]


# ============================================================
# STEP 2: State
# ============================================================

class BoardState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    turn_count: int
    active_agents: list[str]  # Which agents are enabled


# ============================================================
# STEP 3: Generic Agent Node Factory
# ============================================================
# Instead of writing 4 separate functions, we write ONE factory
# that creates a node for any agent config.

def get_model(temperature=0.7):
    return ChatOpenAI(
        model=os.getenv("LLM_MODEL", "deepseek-chat"),
        temperature=temperature,
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def make_agent_node(agent_config: dict):
    """
    Factory: creates a LangGraph node function for an agent.
    
    This is a closure — the inner function 'captures' agent_config
    so each node knows which agent it represents.
    """
    def node_fn(state: BoardState) -> dict:
        model = get_model(agent_config["temperature"])
        messages = [SystemMessage(content=agent_config["prompt"])] + state["messages"]
        response = model.invoke(messages)
        return {
            "messages": [AIMessage(content=response.content, name=agent_config["name"])],
            "turn_count": state["turn_count"] + 1,
        }
    return node_fn


# ============================================================
# STEP 4: Router — Round Robin Through Active Agents
# ============================================================

def router(state: BoardState) -> str:
    """Pick the next agent in round-robin order, or stop."""
    active = state["active_agents"]
    turn = state["turn_count"]
    
    # Each active agent gets one turn per round
    if turn >= len(active):
        return "end"
    
    # Next agent
    return active[turn].lower()


# ============================================================
# STEP 5: Build the Graph
# ============================================================

def build_board_graph(active_agents: list[str] = None):
    """
    Build a LangGraph for the advisory board.
    
    Args:
        active_agents: List of agent names to include.
                      Defaults to all four.
    """
    if active_agents is None:
        active_agents = [a["name"] for a in AGENTS]
    
    # Filter to only active agents
    active_configs = [a for a in AGENTS if a["name"] in active_agents]
    
    builder = StateGraph(BoardState)
    
    # Add a node for each active agent
    for agent in active_configs:
        builder.add_node(agent["name"].lower(), make_agent_node(agent))
    
    # Router node
    builder.add_node("router", lambda state: {})
    builder.set_entry_point("router")
    
    # Router edges
    route_map = {a["name"].lower(): a["name"].lower() for a in active_configs}
    route_map["end"] = END
    builder.add_conditional_edges("router", router, route_map)
    
    # Each agent -> back to router
    for agent in active_configs:
        builder.add_edge(agent["name"].lower(), "router")
    
    return builder.compile()


# ============================================================
# STEP 6: Run the Full Board
# ============================================================

topic = "I want to build a tool that helps teachers create interactive coding tutorials."

print("=" * 60)
print("PART 4: Full Advisory Board (4 Agents)")
print("=" * 60)
print(f"\nTopic: {topic}")
print("-" * 60)

# All four agents
graph = build_board_graph()
result = graph.invoke({
    "messages": [HumanMessage(content=topic, name="User")],
    "turn_count": 0,
    "active_agents": ["Strategist", "Skeptic", "Optimist", "Pragmatist"],
})

print("\n--- FULL BOARD ---\n")
for msg in result["messages"]:
    if isinstance(msg, HumanMessage):
        continue  # Skip the original question
    print(f"[{msg.name}]: {msg.content}\n")


# ============================================================
# STEP 7: Disable an Agent — Watch the Dynamic Change
# ============================================================

print("=" * 60)
print("NOW WITHOUT THE SKEPTIC (echo chamber effect):")
print("=" * 60)

graph_no_skeptic = build_board_graph(active_agents=["Strategist", "Optimist", "Pragmatist"])
result2 = graph_no_skeptic.invoke({
    "messages": [HumanMessage(content=topic, name="User")],
    "turn_count": 0,
    "active_agents": ["Strategist", "Optimist", "Pragmatist"],
})

print()
for msg in result2["messages"]:
    if isinstance(msg, HumanMessage):
        continue
    print(f"[{msg.name}]: {msg.content}\n")

print("-" * 60)
print("KEY INSIGHTS:")
print("  1. Agent nodes are created from data (configs), not hardcoded")
print("  2. make_agent_node is a factory — one function creates any agent")
print("  3. The router does round-robin through active_agents list")
print("  4. Removing the Skeptic changes the group dynamic visibly")
print("  5. This is the foundation — add/remove agents by editing the list")
