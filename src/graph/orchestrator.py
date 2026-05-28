"""
Part 3 & 4: Multi-Agent Orchestrator
======================================

This is the LangGraph graph that orchestrates the advisory board.
Each agent is a node. The router decides who speaks next.
Human input is handled via an interrupt.
"""

import os
from typing import Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langgraph.graph import StateGraph, END

from .state import BoardState
from ..agents.config import AgentConfig, ALL_AGENTS

load_dotenv()


def get_model(temperature: float = 0.7):
    """Create a chat model."""
    return ChatOpenAI(
        model=os.getenv("LLM_MODEL", "deepseek-chat"),
        temperature=temperature,
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def make_agent_node(agent_config: AgentConfig):
    """
    Create a graph node for an agent.
    
    Each node:
    1. Reads the full conversation from state
    2. Prepends the agent's system prompt
    3. Calls the LLM
    4. Returns the response tagged with the agent's name
    """
    def agent_node(state: BoardState) -> dict:
        model = get_model(agent_config.temperature)
        
        # Build messages: system prompt + conversation history
        messages = [SystemMessage(content=agent_config.system_prompt)]
        messages.extend(state["messages"])
        
        # Call the model
        response = model.invoke(messages)
        
        # Tag the response with the agent's name
        tagged_message = AIMessage(
            content=response.content,
            name=agent_config.name,
        )
        
        return {
            "messages": [tagged_message],
            "turn_count": state["turn_count"] + 1,
        }
    
    return agent_node


def router(state: BoardState) -> str:
    """
    Decide what happens next: another agent speaks, or we wait for the human.
    
    Turn-taking logic:
    - Agents speak in round-robin order (Strategist -> Skeptic -> Optimist -> Pragmatist)
    - Only enabled agents get a turn
    - After all enabled agents have spoken, wait for human input
    - Respects max_turns limit
    """
    turn_count = state["turn_count"]
    max_turns = state.get("max_turns", 4)
    active_agents = state.get("active_agents", [a.name for a in ALL_AGENTS])
    
    # If we've hit the turn limit, stop
    if turn_count >= max_turns:
        return "human"
    
    # If we've hit the limit of active agents for this round, stop
    if turn_count >= len(active_agents):
        return "human"
    
    # Next agent in round-robin
    next_agent = active_agents[turn_count % len(active_agents)]
    return next_agent.lower()


def create_advisory_board_graph(
    agents: list[AgentConfig] = None,
    max_turns: int = 4,
) -> StateGraph:
    """
    Build the advisory board LangGraph.
    
    Graph structure:
        human_input -> router -> agent_1 -> router -> agent_2 -> ... -> human_input
    
    The router decides who speaks next based on turn count and active agents.
    """
    if agents is None:
        agents = ALL_AGENTS
    
    # Build the graph
    builder = StateGraph(BoardState)
    
    # Add agent nodes
    for agent in agents:
        builder.add_node(agent.name.lower(), make_agent_node(agent))
    
    # Add router node
    def router_node(state: BoardState) -> dict:
        """Router doesn't modify state, just passes through."""
        return {}
    
    builder.add_node("router", router_node)
    
    # Add human node (placeholder — actual input comes from outside)
    def human_node(state: BoardState) -> dict:
        """Reset turn count for next round."""
        return {"turn_count": 0}
    
    builder.add_node("human", human_node)
    
    # Set entry point
    builder.set_entry_point("router")
    
    # Router edges: route to the correct agent or back to human
    agent_names = [a.name.lower() for a in agents]
    route_map = {name: name for name in agent_names}
    route_map["human"] = "human"
    
    builder.add_conditional_edges("router", router, route_map)
    
    # Each agent goes back to router after speaking
    for agent in agents:
        builder.add_edge(agent.name.lower(), "router")
    
    # Human goes to END (we'll re-invoke the graph for each user message)
    builder.add_edge("human", END)
    
    return builder.compile()


def run_board_round(
    graph,
    user_message: str,
    history: list[BaseMessage] = None,
    active_agents: list[str] = None,
    max_turns: int = 4,
) -> tuple[list[BaseMessage], list[AIMessage]]:
    """
    Run one round of the advisory board.
    
    Args:
        graph: Compiled LangGraph
        user_message: The human's message
        history: Previous conversation messages
        active_agents: Which agents are enabled
        max_turns: Max agent responses per round
    
    Returns:
        (full_history, new_agent_messages)
    """
    if history is None:
        history = []
    if active_agents is None:
        active_agents = [a.name for a in ALL_AGENTS]
    
    # Add user message to history
    human_msg = HumanMessage(content=user_message, name="User")
    all_messages = history + [human_msg]
    
    # Run the graph
    initial_state = {
        "messages": all_messages,
        "next_speaker": "",
        "turn_count": 0,
        "max_turns": min(max_turns, len(active_agents)),
        "active_agents": active_agents,
    }
    
    result = graph.invoke(initial_state)
    
    # Extract new agent messages (everything after the human message)
    new_messages = result["messages"][len(all_messages):]
    
    return result["messages"], new_messages
