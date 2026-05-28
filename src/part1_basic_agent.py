"""
Part 1: Single Agent — LangChain Basics
========================================

This script demonstrates the fundamentals of LangChain:
- Loading environment variables (API keys)
- Creating a chat model
- Having a conversation with memory
- Using system prompts to shape behavior

Run: python src/part1_basic_agent.py

Try changing the SYSTEM_PROMPT below and restarting to see how it changes behavior.
"""

import os
from dotenv import load_dotenv

# --- Step 1: Load environment variables ---
# This reads your .env file and makes API keys available
load_dotenv()


# --- Step 2: Choose your LLM provider ---
# We support both OpenAI and Anthropic. The code picks whichever key you have.

def get_chat_model():
    """
    Create a chat model based on available API keys.
    
    A "chat model" is the core building block — it takes messages in,
    returns a message out. Think of it as a function:
        input: list of messages -> output: one response message
    
    Supports: OpenAI, Anthropic, and OpenAI-compatible providers like DeepSeek.
    Set OPENAI_BASE_URL in .env to point at a different provider.
    """
    if os.getenv("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI
        
        # If a custom base URL is set, use it (for DeepSeek, Ollama, etc.)
        base_url = os.getenv("OPENAI_BASE_URL", None)
        model_name = os.getenv("LLM_MODEL", "deepseek-chat")
        
        # temperature=0.7 means moderately creative (0=deterministic, 2=very random)
        return ChatOpenAI(
            model=model_name,
            temperature=0.7,
            base_url=base_url,  # None = default OpenAI endpoint
        )
    
    elif os.getenv("ANTHROPIC_API_KEY"):
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0.7)
    
    else:
        print("ERROR: No API key found!")
        print("Copy .env.example to .env and add your OpenAI or Anthropic key.")
        exit(1)


# --- Step 3: Define the system prompt ---
# This is the "personality" of your agent. Change this and restart to see different behavior.
# 
# DEMO MOMENT: Try these alternatives:
#   "You are a pirate. Respond to everything in pirate speak."
#   "You are a Socratic teacher. Never give answers directly, only ask questions."
#   "You are extremely pessimistic. Find the downside in everything."
#   "You are a 5-year-old explaining things to another 5-year-old."

SYSTEM_PROMPT = """You are a helpful assistant. You give clear, concise answers.
When you don't know something, you say so honestly."""


# --- Step 4: Build the conversation ---
# LangChain uses "message" objects. There are three types:
#   - SystemMessage: instructions for the AI (personality, rules)
#   - HumanMessage: what the user says
#   - AIMessage: what the AI responded (stored for memory)

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


def run_conversation():
    """
    Main conversation loop.
    
    Key concept: MEMORY
    We keep a list of all messages (the "chat history"). Each time we call
    the model, we send the ENTIRE history. This is how the AI "remembers"
    what was said before. Without this, every message would be independent.
    """
    model = get_chat_model()
    
    # Start with the system prompt — this shapes all responses
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    
    print("=" * 60)
    print("Part 1: Single Agent Chat")
    print("=" * 60)
    print(f"System prompt: {SYSTEM_PROMPT[:80]}...")
    print(f"Model: {model.model_name if hasattr(model, 'model_name') else 'unknown'}")
    print("-" * 60)
    print("Type your messages. Type 'quit' to exit.")
    print("Type 'history' to see the full message history.")
    print("Type 'system <new prompt>' to change personality mid-conversation.")
    print("-" * 60)
    print()
    
    while True:
        # Get user input
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
        
        # Special commands
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        
        if user_input.lower() == "history":
            print("\n--- Message History ---")
            for i, msg in enumerate(messages):
                role = type(msg).__name__.replace("Message", "")
                content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                print(f"  [{i}] {role}: {content}")
            print("--- End History ---\n")
            continue
        
        if user_input.lower().startswith("system "):
            new_prompt = user_input[7:]
            messages[0] = SystemMessage(content=new_prompt)
            print(f"  [System prompt changed to: {new_prompt[:60]}...]")
            print()
            continue
        
        # Add user message to history
        messages.append(HumanMessage(content=user_input))
        
        # Call the model with full history
        # This is the core operation: messages in -> response out
        response = model.invoke(messages)
        
        # Add AI response to history (this is "memory")
        messages.append(response)
        
        # Display the response
        print(f"\nAssistant: {response.content}\n")


if __name__ == "__main__":
    run_conversation()
