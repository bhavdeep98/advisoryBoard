"""
Graph State: The shared memory of the advisory board conversation.

In LangGraph, "state" is the data that flows between nodes.
Every node can read and write to it. This is how agents
see each other's messages and the conversation history.
"""

from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class BoardState(TypedDict):
    """
    The state shared across all agent nodes.
    
    - messages: Full conversation history (human + all agents).
      Uses `add_messages` reducer which appends new messages
      rather than replacing the list.
    - next_speaker: Which agent speaks next.
    - turn_count: How many agent turns have happened this round.
    - max_turns: Maximum agent turns per user message.
    - active_agents: List of agent names that are enabled.
    """
    messages: Annotated[list[BaseMessage], add_messages]
    next_speaker: str
    turn_count: int
    max_turns: int
    active_agents: list[str]
