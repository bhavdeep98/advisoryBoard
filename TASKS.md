# Tasks: Advisory Board Playground

## Progress

| Part | Status | Description |
|------|--------|-------------|
| 1 | 🔄 In Progress | Single Agent — LangChain Basics |
| 2 | ⬜ Not Started | Agent with Personality — Configurable Behavior |
| 3 | ⬜ Not Started | Two Agents Talking — LangGraph Basics |
| 4 | ⬜ Not Started | Four Agents Debating — Advisory Board |
| 5 | ⬜ Not Started | Human-in-the-Loop — User Interaction |
| 6 | ⬜ Not Started | Backend + Simple UI — FastAPI & WebSocket |
| 7 | ⬜ Not Started | Configuration Playground — Full Teaching UI |

---

## Part 1: Single Agent — LangChain Basics

**Goal:** Get a working agent in the terminal that responds to messages with memory.

**What you'll learn:**
- How to install and configure LangChain
- What a chat model is and how to call it
- How conversation memory works
- How changing a system prompt changes behavior

**Tasks:**
- [ ] Set up Python virtual environment
- [ ] Install dependencies (langchain, langchain-openai, langchain-anthropic, python-dotenv)
- [ ] Create `.env` with API key
- [ ] Write `src/part1_basic_agent.py` — minimal chat model call
- [ ] Add conversation memory (chat history)
- [ ] Add a system prompt
- [ ] Write tutorial doc: `docs/part1-single-agent.md`
- [ ] Demo moment: change system prompt, show different behavior

**Output:** A Python script you can run in terminal, have a conversation, and see how the system prompt shapes responses.

---

## Part 2: Agent with Personality — Configurable Behavior

**Goal:** Create agents with distinct personalities via system prompts and parameters.

**What you'll learn:**
- Prompt engineering for personality/character
- Effect of temperature on output
- How model choice affects behavior
- Making agents configurable (not hardcoded)

**Tasks:**
- [ ] Create agent config dataclass (name, system_prompt, temperature, model)
- [ ] Write the four advisory board agent configs
- [ ] Build a runner that takes config and produces responses
- [ ] Demo: same question, different temperatures — show output spread
- [ ] Demo: same question, different system prompts — show personality shift
- [ ] Write tutorial doc: `docs/part2-personality.md`

**Output:** Four configurable agent definitions. Run any one in terminal, see its personality.

---

## Part 3: Two Agents Talking — LangGraph Basics

**Goal:** Two agents have a back-and-forth conversation using LangGraph.

**What you'll learn:**
- LangGraph concepts: nodes, edges, state
- How to pass messages between agents
- Graph execution and state management

**Tasks:**
- [ ] Install langgraph
- [ ] Define graph state (shared message history)
- [ ] Create two agent nodes (Strategist + Skeptic)
- [ ] Wire edges: Strategist → Skeptic → Strategist (loop)
- [ ] Add a stop condition (N turns or convergence)
- [ ] Demo: change one agent's prompt, watch conversation shift
- [ ] Write tutorial doc: `docs/part3-two-agents.md`

**Output:** Run the script, give a topic, watch two agents debate it for N turns.

---

## Part 4: Four Agents Debating — Advisory Board

**Goal:** Full advisory board with turn-taking logic.

**What you'll learn:**
- Multi-agent orchestration patterns
- Turn-taking strategies (round-robin, relevance-based, random)
- Agents referencing each other's points
- Enabling/disabling agents dynamically

**Tasks:**
- [ ] Expand graph to four agent nodes
- [ ] Implement turn-taking logic (who speaks next)
- [ ] Agents see full conversation history (can reference each other)
- [ ] Add enable/disable per agent
- [ ] Demo: disable the Skeptic, watch group become echo chamber
- [ ] Write tutorial doc: `docs/part4-advisory-board.md`

**Output:** Full four-agent debate in terminal. Toggle agents on/off.

---

## Part 5: Human-in-the-Loop — User Interaction

**Goal:** You participate in the conversation, agents respond to you.

**What you'll learn:**
- LangGraph interrupt/resume for human input
- Routing messages to specific agents
- Conversation steering patterns

**Tasks:**
- [ ] Add human input node to the graph
- [ ] Implement LangGraph interrupt (pause for user)
- [ ] Allow addressing specific agents ("@Skeptic what do you think?")
- [ ] Agents adapt when user redirects the topic
- [ ] Demo: redirect conversation mid-debate, see agents adapt
- [ ] Write tutorial doc: `docs/part5-human-in-loop.md`

**Output:** Interactive terminal session — you're in the group chat with the agents.

---

## Part 6: Backend + Simple UI — FastAPI & WebSocket

**Goal:** Move from terminal to browser with real-time streaming.

**What you'll learn:**
- FastAPI basics and WebSocket connections
- Streaming LLM responses token-by-token
- Simple frontend that connects via WebSocket
- Session management

**Tasks:**
- [ ] Create FastAPI app with WebSocket endpoint
- [ ] Stream agent responses to frontend
- [ ] Build simple HTML/CSS/JS chat interface
- [ ] Agent messages show with distinct names and colors
- [ ] Handle multiple conversation sessions
- [ ] Demo: open in browser, type message, see agents respond live
- [ ] Write tutorial doc: `docs/part6-backend-ui.md`

**Output:** A web page with a working group chat. Agents respond in real-time.

---

## Part 7: Configuration Playground — Full Teaching UI

**Goal:** Add the config panel so users can tweak agents live.

**What you'll learn:**
- Live configuration hot-reload without restart
- Building interactive teaching interfaces
- State management across config changes
- Preset systems

**Tasks:**
- [ ] Add config panel UI (left side): system prompt editor, temperature slider, model dropdown, toggle
- [ ] WebSocket messages for config updates
- [ ] Backend hot-reloads agent config without losing conversation
- [ ] "What changed?" highlight on responses after config edit
- [ ] Implement presets (Default, Echo Chamber, Chaos, Minimal)
- [ ] Tooltip explanations for each setting
- [ ] Demo: live in class — students change settings, see effects
- [ ] Write tutorial doc: `docs/part7-playground.md`

**Output:** The full teaching playground. Two panels, live config, presets, ready for demos.
