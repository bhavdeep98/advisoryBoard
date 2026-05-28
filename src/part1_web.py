"""
Part 1 Web Demo: Single Agent Chat in the Browser
===================================================

Run: python src/part1_web.py
Then open: http://localhost:8000
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import uvicorn

load_dotenv()

app = FastAPI()

# Serve static files (index.html)
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

# Store conversations per session (in-memory, resets on restart)
conversations = {}


def get_model(temperature: float = 0.7):
    """Create a chat model with the given temperature."""
    return ChatOpenAI(
        model=os.getenv("LLM_MODEL", "deepseek-chat"),
        temperature=temperature,
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


@app.post("/api/chat")
async def chat(request: Request):
    """Handle a chat message."""
    data = await request.json()

    user_message = data.get("message", "")
    system_prompt = data.get("system_prompt", "You are a helpful assistant.")
    temperature = float(data.get("temperature", 0.7))
    session_id = data.get("session_id", "default")

    if session_id not in conversations:
        conversations[session_id] = []

    history = conversations[session_id]

    messages = [SystemMessage(content=system_prompt)]
    messages.extend(history)
    messages.append(HumanMessage(content=user_message))

    model = get_model(temperature)
    response = model.invoke(messages)

    history.append(HumanMessage(content=user_message))
    history.append(response)

    return JSONResponse({
        "response": response.content,
        "history_length": len(history),
    })


@app.post("/api/clear")
async def clear(request: Request):
    """Clear conversation history."""
    data = await request.json()
    session_id = data.get("session_id", "default")
    conversations[session_id] = []
    return JSONResponse({"status": "cleared"})


# Serve index.html at root
from fastapi.responses import FileResponse

@app.get("/")
async def index():
    return FileResponse(static_dir / "index.html")


if __name__ == "__main__":
    print("Starting Part 1 Web Demo...")
    print("Open http://localhost:8000 in your browser")
    print("Press Ctrl+C to stop")
    uvicorn.run(app, host="0.0.0.0", port=8000)
