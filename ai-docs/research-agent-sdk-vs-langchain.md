---
version: 0.1.0
updated: 2025-12-23
rationale: |
  Deep comparison of Claude Agent SDK vs LangChain/LangGraph for building AI agents.
  Research question: Are they complementary or competitive? When to use each?
  Conclusion: Complementary — different philosophies, overlapping MCP ecosystem.
sources:
  - url: https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
    name: Anthropic Engineering Blog
  - url: https://blog.langchain.com/langchain-langgraph-1dot0/
    name: LangChain 1.0 Announcement
  - url: https://enhancial.substack.com/p/choosing-the-right-ai-framework-a
    name: AI Framework Comparison 2025
  - url: https://clickhouse.com/blog/how-to-build-ai-agents-mcp-12-frameworks
    name: 12 Agent Frameworks Compared
linked_files:
  - ai-docs/plugins-experiment.md
---

# Claude Agent SDK vs LangChain: A Deep Comparison

## TL;DR

| Dimension | Claude Agent SDK | LangChain/LangGraph |
|-----------|------------------|---------------------|
| **Philosophy** | "Give Claude a computer" | "Compose anything with anything" |
| **Model Support** | Claude only | Model-agnostic (100+ providers) |
| **Complexity** | Opinionated, low boilerplate | Flexible, more setup |
| **Best For** | Production agents with Claude | Prototypes, multi-model, custom workflows |
| **MCP Support** | First-class (Anthropic created MCP) | Supported via integrations |

**Verdict: Complementary, not competitive.** Different tools for different jobs, unified by MCP.

---

## 1. Origins & Philosophy

### Claude Agent SDK

> "The key design principle is to give your agents a computer, allowing them to work like humans do."
> — Anthropic Engineering

- **Born from:** Claude Code (renamed September 2025)
- **Core insight:** Claude became effective at non-coding tasks when given terminal + file system
- **Design:** Opinionated, production-focused, Claude-native
- **Metaphor:** A developer with a terminal

### LangChain/LangGraph

> "LangChain is the fastest way to build an AI agent — provider agnostic, middleware for customization."
> — LangChain Blog

- **Born from:** Need to compose LLM components (2022)
- **Core insight:** LLMs need orchestration, tools, memory, chains
- **Design:** Flexible, component-based, model-agnostic
- **Metaphor:** LEGO blocks for AI

**Key Difference:** Claude Agent SDK assumes Claude. LangChain assumes nothing.

### Claude Agent SDK = Claude Code's Engine, Exposed

```
┌─────────────────────────────────────────────────────────┐
│                    CLAUDE CODE                          │
│         (Anthropic's general-purpose coding CLI)        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────────────────────────────────────────┐   │
│   │            CLAUDE AGENT SDK                     │   │
│   │         (The engine underneath)                 │   │
│   │                                                 │   │
│   │   • Agent loop (gather → act → verify)         │   │
│   │   • Tool system (Bash, Read, Write, Edit...)   │   │
│   │   • Context compaction                         │   │
│   │   • Subagents                                  │   │
│   │   • MCP integration                            │   │
│   │   • Session persistence                        │   │
│   └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**What Anthropic did:** They realized Claude Code's internals were so good at general agent tasks (not just coding) that they extracted and released them as an SDK.

### Your Own "Claude Code" for X

| You Build | What It Is |
|-----------|------------|
| Email Agent | Claude Code but for triaging/drafting emails |
| Research Agent | Claude Code but for deep web research |
| Data Pipeline Agent | Claude Code but for ETL workflows |
| Customer Support Agent | Claude Code but for ticket resolution |

**You get for free:**
- The agent loop (already learned, battle-tested)
- Tool execution
- Context management
- Self-verification patterns

**You customize:**
- Which tools are available
- System prompt / persona
- MCP servers (data sources)
- Guardrails / allowed actions

### Not Fine-Tuning

Important distinction: You're not training or fine-tuning Claude. You're **configuring the harness** around it.

```python
# Minimal example - your own "Claude Code for emails"
from claude_agent_sdk import Agent

agent = Agent(
    model="claude-sonnet-4-5",
    system="You are an email assistant. You triage, draft, and organize.",
    tools=["Read", "Write", "Bash"],  # Subset of tools
    mcp_servers=["gmail", "calendar"]  # Your data sources
)

agent.run("Summarize my unread emails and draft replies")
```

That's it. The loop, verification, context handling — all inherited from Claude Code's proven patterns.

---

## 2. Architecture

### Claude Agent SDK: The Agent Loop

```
┌─────────────────────────────────────────┐
│            CLAUDE AGENT LOOP            │
├─────────────────────────────────────────┤
│                                         │
│   1. GATHER CONTEXT                     │
│      └─ Read files, search, query MCPs  │
│                                         │
│   2. TAKE ACTION                        │
│      └─ Write code, run commands, edit  │
│                                         │
│   3. VERIFY WORK                        │
│      └─ Self-check, test, validate      │
│                                         │
│   4. REPEAT                             │
│      └─ Until task complete             │
│                                         │
└─────────────────────────────────────────┘
```

**Key Features:**
- Subagents for parallelization and context isolation
- Context compaction for long-running sessions
- Built-in tools: Bash, Read, Write, Edit, Glob, Grep
- Code generation as first-class output

### LangChain: Chain-Based (DAGs)

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Input   │ → │  Chain   │ → │  Output  │
└──────────┘    └──────────┘    └──────────┘
                    │
              ┌─────┴─────┐
              │   Tools   │
              │  Memory   │
              │ Retrievers│
              └───────────┘
```

**Key Features:**
- LCEL (LangChain Expression Language) for declarative pipelines
- Rich component library (loaders, splitters, vector stores)
- 100+ model integrations
- Middleware hooks for customization

### LangGraph: Graph-Based (Cycles)

```
        ┌─────────────────────────────────┐
        │          STATE GRAPH            │
        ├─────────────────────────────────┤
        │                                 │
        │    ┌───────┐    ┌───────┐      │
        │    │ Node  │───→│ Node  │      │
        │    └───┬───┘    └───┬───┘      │
        │        │            │          │
        │        ↓            ↓          │
        │    ┌───────┐    ┌───────┐      │
        │    │ Node  │←───│ Node  │      │
        │    └───────┘    └───────┘      │
        │         ↑___________↓          │
        │           (cycles!)            │
        └─────────────────────────────────┘
```

**Key Features:**
- First-class state management
- Loops, branching, conditional flows
- Human-in-the-loop interrupts
- Time-travel debugging
- Durable execution (survives failures)

**2025 Recommendation:** LangGraph for all new agent implementations.

---

## 3. Comparison Matrix

| Feature | Claude Agent SDK | LangChain | LangGraph |
|---------|------------------|-----------|-----------|
| **Architecture** | Agent loop | Linear chains (DAG) | Graph with cycles |
| **State Management** | Session-based | Pass-through | First-class persistent |
| **Model Support** | Claude only | 100+ providers | 100+ providers |
| **Tool Integration** | Built-in + MCP | Custom + integrations | Custom + integrations |
| **Memory** | Context compaction | Various memory types | Short + long-term |
| **Human-in-the-Loop** | Via hooks | Limited | Built-in interrupts |
| **Debugging** | Standard + hooks | Standard logging | Time-travel debugging |
| **Multi-Agent** | Subagents | Basic | Supervisor, Swarm, Hierarchical |
| **Code Generation** | First-class | Via tools | Via tools |
| **Learning Curve** | Low | Medium | High |
| **Production Ready** | Yes (battle-tested) | Good for prototypes | Enterprise-scale |

---

## 4. MCP: The Unifying Layer

Both frameworks support **Model Context Protocol (MCP)** — the standardized way to connect agents to external services.

```
┌─────────────────────────────────────────────────────────┐
│                    MCP ECOSYSTEM                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────┐         ┌─────────────────────────┐  │
│   │ Claude      │         │  MCP Servers            │  │
│   │ Agent SDK   │◄───────►│  • Slack                │  │
│   └─────────────┘         │  • GitHub               │  │
│                           │  • Google Drive         │  │
│   ┌─────────────┐         │  • Asana                │  │
│   │ LangChain/  │◄───────►│  • PostgreSQL           │  │
│   │ LangGraph   │         │  • Custom servers       │  │
│   └─────────────┘         └─────────────────────────┘  │
│                                                         │
│   ┌─────────────┐                                      │
│   │ OpenAI      │◄───────►  (Same MCP servers)         │
│   │ Agents SDK  │                                      │
│   └─────────────┘                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Key Insight:** MCP is framework-agnostic. An MCP server you build works with Claude Agent SDK, LangChain, OpenAI Agents SDK, and any MCP-compatible client.

---

## 5. When to Use What

### Use Claude Agent SDK When:

| Scenario | Why |
|----------|-----|
| Building with Claude exclusively | Native integration, optimized |
| Coding/development agents | Born from Claude Code, excels here |
| Production single-agent systems | Battle-tested, low boilerplate |
| Need terminal/file system access | Built-in, first-class |
| Want minimal setup | Opinionated = fewer decisions |
| Long-running autonomous tasks | Context compaction, session persistence |

**Example:** A code review agent that clones repos, runs tests, writes reports.

### Use LangChain When:

| Scenario | Why |
|----------|-----|
| Rapid prototyping | Quick iteration, rich components |
| Multi-model strategy | Swap models without code changes |
| RAG pipelines | Best-in-class retrieval components |
| Need specific integrations | 100+ pre-built connectors |
| Learning/experimenting | Great docs, large community |

**Example:** A document QA system that might use GPT-4 today, Claude tomorrow.

### Use LangGraph When:

| Scenario | Why |
|----------|-----|
| Complex multi-agent systems | Supervisor, swarm, hierarchical patterns |
| Need human-in-the-loop | Built-in interrupts and approvals |
| Stateful workflows | First-class state management |
| Production enterprise agents | Durable execution, debugging |
| Custom control flow | Loops, branches, conditionals |

**Example:** A customer support system with triage agent → specialist agents → escalation paths.

---

## 6. Complementary Usage Patterns

### Pattern 1: Claude Agent SDK + LangChain Components

```python
# Use LangChain for retrieval, Claude Agent SDK for execution
from langchain_community.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic
from claude_agent_sdk import Agent

# LangChain handles the RAG part
vectorstore = Chroma.from_documents(docs)
retriever = vectorstore.as_retriever()

# Claude Agent SDK handles the agent execution
agent = Agent(
    model="claude-sonnet-4-5",
    tools=[retriever_tool],  # Wrap retriever as tool
    system="You are a research assistant..."
)
```

### Pattern 2: LangGraph Orchestration + Claude Agent SDK Nodes

```python
# LangGraph manages the workflow, Claude Agent SDK powers specific nodes
from langgraph.graph import StateGraph
from claude_agent_sdk import query

def coding_node(state):
    # Use Claude Agent SDK for coding tasks
    result = query(
        prompt=state["task"],
        options={"tools": ["Bash", "Read", "Write", "Edit"]}
    )
    return {"code": result}

graph = StateGraph(AgentState)
graph.add_node("coder", coding_node)  # Claude Agent SDK
graph.add_node("reviewer", review_node)  # Could be different model
```

### Pattern 3: Shared MCP Servers

```json
// Same .mcp.json works for both frameworks
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"]
    },
    "slack": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-slack"]
    }
  }
}
```

---

## 7. The 2025 Landscape

### Framework Convergence

> "Despite being developed by different teams, many agent frameworks are converging in architecture."
> — Medium, State of AI Agent Frameworks

All major frameworks now share:
- Tool/function calling
- Reasoning loops
- Memory systems
- MCP support (increasingly)

### Differentiation Points

| Framework | Unique Strength |
|-----------|-----------------|
| **Claude Agent SDK** | Production-grade infrastructure for Claude |
| **OpenAI Agents SDK** | Fast multi-agent coordination with handoffs |
| **LangGraph** | Maximum control for complex workflows |
| **MCP** | Standardized data connectivity (works with all) |

---

## 8. Recommendations for Your Use Case

Given your context (learning LangChain, exploring Claude Agent SDK):

### Short-Term: Learn Both

| Week | Focus | Goal |
|------|-------|------|
| 1 | LangChain basics | Understand chains, LCEL, components |
| 2 | LangGraph | Build a stateful agent with loops |
| 3 | Claude Agent SDK | Build a coding/research agent |
| 4 | Integration | Connect them via MCP |

### Long-Term: Specialize by Task

| Task Type | Recommended Framework |
|-----------|----------------------|
| Coding agents | Claude Agent SDK |
| Multi-model pipelines | LangChain |
| Complex workflows | LangGraph |
| Quick prototypes | LangChain |
| Production Claude agents | Claude Agent SDK |

### MCP as the Bridge

Invest in MCP servers — they work with everything. Build once, use everywhere.

---

## 9. Key Takeaways

1. **Not competitive, complementary.** Different philosophies, overlapping ecosystem.

2. **Claude Agent SDK = opinionated Claude.** Best for production agents when you're committed to Claude.

3. **LangChain = flexible composition.** Best for prototypes, multi-model, rich integrations.

4. **LangGraph = production orchestration.** Best for complex, stateful, multi-agent systems.

5. **MCP unifies everything.** Framework-agnostic protocol for tool integration.

6. **2025 trend: convergence.** All frameworks are becoming more similar in architecture.

7. **Your choice depends on:**
   - Model commitment (Claude-only vs multi-model)
   - Workflow complexity (linear vs graph)
   - Production requirements (durability, debugging, human-in-loop)

---

## 10. Practical FAQ

### Q: Do I need an API key or does my Max subscription work?

**Both work.** You choose at setup:

| Method | How | Billing |
|--------|-----|---------|
| **Subscription** | "Log in with your subscription account" | Comes from your Max plan quota |
| **API Key** | `export ANTHROPIC_API_KEY="sk-..."` | Pay-as-you-go via Anthropic Console |

With Max subscription, you get ~$150+ worth of API usage for $100-200/month. Good for development and moderate production use.

### Q: Does the SDK update when Claude Code updates?

**Yes.** The SDK IS Claude Code's engine. When Claude Code gets new features (context compaction improvements, new tools, etc.), the SDK gets them too.

```bash
# Update SDK
pip install --upgrade claude-agent-sdk  # Python
npm update @anthropic-ai/claude-agent-sdk  # TypeScript
```

### Q: What about multi-modal (images, audio, video)?

| Modality | Support | Notes |
|----------|---------|-------|
| **Text** | Full | Native |
| **Images** | Full | Up to 100 images per API request, vision analysis |
| **Audio** | Indirect | Transcribe first (Whisper), then process text |
| **Video** | No | Use Gemini for video understanding, then pass to Claude |

**Practical workflow for audio:**
```python
# 1. Transcribe with Whisper
transcript = whisper.transcribe("meeting.mp3")

# 2. Analyze with Claude Agent SDK
agent.run(f"Analyze this meeting transcript: {transcript}")
```

Claude excels at text analysis — pair it with specialized tools for other modalities.

---

## 11. Next Steps

- [ ] Build a simple agent with Claude Agent SDK (`/new-sdk-app`)
- [ ] Build the same agent with LangGraph
- [ ] Compare: boilerplate, debugging, performance
- [ ] Create a shared MCP server both can use
- [ ] Document findings in this repo
