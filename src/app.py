"""
Parts 5-7: Full Advisory Board Playground
==========================================

The complete web app:
- Four agents debating in a group chat
- Human-in-the-loop (you're in the conversation)
- Live configuration (change prompts, temperature, toggle agents)
- Presets for teaching demos

Run: python src/app.py
Open: http://localhost:8000
"""

import os
import json
from pathlib import Path
from copy import deepcopy
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, BaseMessage
import uvicorn

load_dotenv()

app = FastAPI()

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# --- Agent configs (mutable per session) ---

from agents.config import AgentConfig, ALL_AGENTS

# Store per-session state
sessions: dict[str, dict] = {}


def get_session(session_id: str) -> dict:
    """Get or create a session."""
    if session_id not in sessions:
        sessions[session_id] = {
            "history": [],
            "agents": [deepcopy(a) for a in ALL_AGENTS],
        }
    return sessions[session_id]


def get_model(temperature: float = 0.7):
    """Create a chat model."""
    return ChatOpenAI(
        model=os.getenv("LLM_MODEL", "deepseek-chat"),
        temperature=temperature,
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


# --- WebSocket for real-time chat ---

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    session = get_session(session_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            
            if action == "chat":
                await handle_chat(websocket, session, data)
            elif action == "update_agent":
                await handle_update_agent(websocket, session, data)
            elif action == "clear":
                session["history"] = []
                await websocket.send_json({"type": "cleared"})
            elif action == "get_agents":
                await websocket.send_json({
                    "type": "agents",
                    "agents": [a.to_dict() for a in session["agents"]],
                })
    except WebSocketDisconnect:
        pass


async def handle_chat(websocket: WebSocket, session: dict, data: dict):
    """Process a user message and get responses from enabled agents."""
    user_message = data.get("message", "")
    if not user_message:
        return
    
    # Add user message to history
    human_msg = HumanMessage(content=user_message, name="User")
    session["history"].append(human_msg)
    
    # Send acknowledgment
    await websocket.send_json({
        "type": "user_message",
        "name": "You",
        "content": user_message,
    })
    
    # Get enabled agents
    active_agents = [a for a in session["agents"] if a.enabled]
    
    if not active_agents:
        await websocket.send_json({
            "type": "system",
            "content": "No agents are enabled. Toggle at least one agent on.",
        })
        return
    
    # Each active agent responds in sequence
    for agent in active_agents:
        # Send typing indicator
        await websocket.send_json({
            "type": "typing",
            "name": agent.name,
        })
        
        # Build messages for this agent
        messages = [SystemMessage(content=agent.system_prompt)]
        messages.extend(session["history"])
        
        # Call the model
        model = get_model(agent.temperature)
        
        try:
            response = model.invoke(messages)
            
            # Tag and store
            agent_msg = AIMessage(content=response.content, name=agent.name)
            session["history"].append(agent_msg)
            
            # Send to client
            await websocket.send_json({
                "type": "agent_message",
                "name": agent.name,
                "role": agent.role,
                "content": response.content,
                "color": agent.color,
                "avatar": agent.avatar,
            })
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "name": agent.name,
                "content": f"Error: {str(e)}",
            })
    
    # Signal round complete
    await websocket.send_json({"type": "round_complete"})


async def handle_update_agent(websocket: WebSocket, session: dict, data: dict):
    """Update an agent's configuration."""
    agent_name = data.get("name")
    updates = data.get("updates", {})
    
    for agent in session["agents"]:
        if agent.name == agent_name:
            if "system_prompt" in updates:
                agent.system_prompt = updates["system_prompt"]
            if "temperature" in updates:
                agent.temperature = float(updates["temperature"])
            if "enabled" in updates:
                agent.enabled = bool(updates["enabled"])
            break
    
    await websocket.send_json({
        "type": "agent_updated",
        "name": agent_name,
        "agents": [a.to_dict() for a in session["agents"]],
    })


# --- REST endpoints ---

@app.post("/api/preset")
async def apply_preset(request: Request):
    """Apply a preset configuration."""
    data = await request.json()
    session_id = data.get("session_id", "default")
    preset_name = data.get("preset")
    
    session = get_session(session_id)
    
    presets = {
        "default": ALL_AGENTS,
        "echo_chamber": [
            AgentConfig(name="Agreeer 1", role="Agrees with everything", 
                       system_prompt="You agree with everything enthusiastically. Say 'Great idea!' and add minor supportive points. Never disagree.",
                       temperature=0.7, color="#4ECDC4", avatar="👍"),
            AgentConfig(name="Agreeer 2", role="Also agrees", 
                       system_prompt="You agree with everything. Support the previous speakers. Add 'Absolutely!' and similar affirmations.",
                       temperature=0.7, color="#6BCB77", avatar="👍"),
            AgentConfig(name="Agreeer 3", role="Agrees too", 
                       system_prompt="You enthusiastically agree with all ideas. Never push back. Say things like 'Love it!' and 'Brilliant!'",
                       temperature=0.7, color="#FFD93D", avatar="👍"),
        ],
        "chaos": [
            AgentConfig(name="Wildcard", role="Unpredictable", 
                       system_prompt="You are completely unpredictable. Sometimes agree, sometimes disagree violently, sometimes go on tangents. Be chaotic.",
                       temperature=2.0, color="#E94560", avatar="🎲"),
            AgentConfig(name="Contrarian", role="Disagrees with everything", 
                       system_prompt="You disagree with EVERYTHING. Whatever was said, take the opposite position. Be dramatic about it.",
                       temperature=1.5, color="#9B59B6", avatar="🔥"),
            AgentConfig(name="Philosopher", role="Goes deep", 
                       system_prompt="You turn every practical question into a deep philosophical inquiry. Ask existential questions. Reference obscure philosophers.",
                       temperature=1.8, color="#3498DB", avatar="🤔"),
        ],
        "minimal": [
            AgentConfig(name="Assistant", role="Simple helper", 
                       system_prompt="You are a helpful assistant. Give clear, concise answers.",
                       temperature=0.7, color="#888888", avatar="💬"),
        ],
    }
    
    if preset_name in presets:
        session["agents"] = [deepcopy(a) for a in presets[preset_name]]
        session["history"] = []
        return JSONResponse({
            "status": "applied",
            "preset": preset_name,
            "agents": [a.to_dict() for a in session["agents"]],
        })
    
    return JSONResponse({"status": "error", "message": "Unknown preset"}, status_code=400)


@app.get("/")
async def index():
    return FileResponse(static_dir / "playground.html")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    
    print("Starting Advisory Board Playground...")
    print("Open http://localhost:8000 in your browser")
    print("Press Ctrl+C to stop")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
