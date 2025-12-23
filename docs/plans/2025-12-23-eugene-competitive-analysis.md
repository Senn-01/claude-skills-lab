---
description: Competitive analysis and design inspiration for Eugene - studying Things 3, Notion, Saner.AI, Linear, and the agent-first future
version: 0.1.0
status: research
created: 2025-12-23
parent: 2025-12-23-eugene-design.md
changelog:
  - version: 0.1.0
    date: 2025-12-23
    changes:
      - Initial competitive analysis
      - Studied Things 3, Notion, Saner.AI, Linear
      - Researched multi-agent architectures
      - Defined Eugene's unique positioning
linked_files:
  - docs/plans/2025-12-23-eugene-design.md
---

# Eugene: Competitive Analysis & Design Inspiration

## Philosophy

> "Software-as-a-Service platforms that force users to click through slow UIs will be disrupted by agents that interact with the database/API directly."

> "The best UIs will become prompt interfaces where the user states an intent, and a swarm of agents executes the CRUD operations in the background."

Eugene is not another productivity app. It is **the interface layer** between human intent and structured action. Voice in, results out.

---

## Competitive Landscape

### 1. Things 3 — GTD Mastery

**What they do well:**

| Element | Implementation | Why it works |
|---------|----------------|--------------|
| **Areas** | Top-level containers for life domains (Work, Personal, Health) | Separates concerns; filters noise |
| **Projects** | Completable goals within areas | Everything has a home |
| **Tags** | Context-based filtering (@desk, @errands, @calls) | GTD "next action by context" |
| **Today/Anytime/Someday** | Temporal buckets | Reduces decision fatigue |
| **Logbook** | Completed items archive | Sense of progress |
| **Weekly Review** | Built-in review workflow | Keeps system clean |

**Key insight:** Things 3 succeeds because it **constrains choice**. No custom fields, no databases, no complexity. Just Areas → Projects → Tasks → Tags.

**What Eugene steals:**
- **Temporal buckets**: inbox → today → someday → done
- **Areas concept**: High-level life domains for filtering
- **Review as ritual**: Built-in prompt to process inbox
- **Logbook**: Archive of completed work for trends

**What Eugene does differently:**
- Voice-first capture (Things requires manual entry)
- Agent suggests structure (Things requires user to categorize)
- Cross-device via Telegram (Things is Apple-only)

---

### 2. Notion — Database Flexibility

**What they do well:**

| Element | Implementation | Why it works |
|---------|----------------|--------------|
| **Databases** | Structured collections of pages | Everything queryable |
| **Properties** | Typed fields (text, date, select, relation) | Consistent metadata |
| **Relations** | Link databases together | Projects ↔ Tasks ↔ Sprints |
| **Rollups** | Aggregate data from relations | Progress %, counts |
| **Views** | Same data, different presentations (table, board, calendar, timeline) | Context-appropriate display |
| **Formulas** | Computed fields | Smart defaults, auto-status |
| **Templates** | Pre-configured pages | Consistent structure |

**Key insight:** Notion's power is **relations + views**. One database, infinite perspectives. But the flexibility creates paralysis — users spend more time building systems than using them.

**What Eugene steals:**
- **Relation pattern**: Inbox items → Projects → Journal notes (linked entities)
- **Multiple views**: Same projects shown as list, board, or cost/benefit matrix
- **Rollups concept**: Project progress from linked tasks
- **Properties as metadata**: Tags, status, dates as typed fields

**What Eugene does differently:**
- No building required (Notion requires setup)
- Agent creates structure (Notion requires user to design)
- Single purpose (Notion tries to be everything)
- Voice interface (Notion is click-heavy)

---

### 3. Saner.AI — Direct Competitor

**What they do well:**

| Element | Implementation | Why it works |
|---------|----------------|--------------|
| **Universal inbox** | Notes, tasks, emails, calendar in one place | Reduces context-switching |
| **Voice-to-task** | Speak → structured task | Frictionless capture |
| **Morning plan** | AI suggests daily priorities | Decision support |
| **Brain dump processing** | Messy thoughts → structured actions | Handles chaos |
| **Semantic search** | Find by meaning, not keywords | Natural retrieval |
| **Multi-model** | GPT-4, Claude, Gemini options | User choice |
| **ADHD-friendly** | Minimal UI, no tags/folders required | Reduces overwhelm |

**Key insight:** Saner.AI nails the **capture + process loop** for neurodivergent users. They understand that the enemy is not lack of features — it's cognitive load.

**What Eugene steals:**
- **Morning plan concept**: "You have X items, here's what to prioritize"
- **Brain dump → action**: Accept messy input, output structure
- **Semantic search**: Embeddings for journal retrieval
- **ADHD-friendly defaults**: Auto-organize, no manual filing

**Where Eugene differentiates:**

| Saner.AI | Eugene |
|----------|--------|
| Web/mobile app | Telegram + Web (no app install for capture) |
| General productivity | GTD-specific with cost/benefit matrix |
| Email-centric | Voice-first with multimodal (images, links) |
| Generic AI | LangGraph supervisor with specialized sub-agents |
| SaaS | Open architecture (self-hostable) |
| Morning planning | Anytime voice-driven sorting |
| Static UI | Retrofuturism CRT aesthetic (delight factor) |

**Eugene's edge:** Telegram as capture surface means zero friction. No app to open, no login required. Just message Eugene.

---

### 4. Linear — Engineering-Grade Simplicity

**What they do well:**

| Element | Implementation | Why it works |
|---------|----------------|--------------|
| **Speed** | Sub-100ms interactions | No waiting, flow state preserved |
| **Keyboard-first** | Every action has a shortcut | Power users fly |
| **Cmd+K** | Universal command palette | One entry point for all actions |
| **Opinionated defaults** | Issues, Projects, Cycles (that's it) | No setup paralysis |
| **Visual polish** | Beautiful, consistent design | Joy in use |
| **Warp mode** | Keyboard navigation overlay | Discoverability |

**Key insight:** Linear proves that **constraints + speed = adoption**. They don't try to be Jira. They picked a lane (dev teams) and optimized ruthlessly.

**What Eugene steals:**
- **Speed obsession**: Every interaction under 200ms
- **Command palette**: Cmd+K for power users alongside voice
- **Keyboard shortcuts**: Full keyboard navigation in web UI
- **Opinionated structure**: Inbox, Projects, Journal, Trends (that's it)
- **Visual delight**: Retrofuturism aesthetic with same polish level

**What Eugene does differently:**
- Voice as primary interface (Linear is keyboard)
- Personal productivity (Linear is team collaboration)
- Cost/benefit matrix (Linear has cycles/sprints)

---

### 5. Multi-Agent Architecture — The Future

**What the research shows:**

| Trend | Evidence | Implication for Eugene |
|-------|----------|------------------------|
| **Supervisor pattern** | LangGraph docs, CrewAI adoption | Eugene as supervisor routing to specialists |
| **Human-in-the-loop** | 2025 agent frameworks prioritize this | User confirms agent suggestions |
| **Role-based agents** | CrewAI's model, 60% of Fortune 500 | Capture/Inbox/Project/Journal agents |
| **Swarm collaboration** | OpenAI Swarm, multi-agent systems | Future: agents collaborate on complex requests |
| **Enterprise adoption** | 35% productivity gains reported | Eugene architecture is enterprise-ready |

**What Eugene implements:**
- **Supervisor agent** (Eugene) routes to specialized sub-agents
- **Human-in-the-loop** for sorting decisions
- **Expandable architecture**: Add agents without rewrite
- **Memory across sessions**: PostgreSQL checkpointing

---

### 6. Conversational UI — The Interface Paradigm

**Key patterns emerging:**

| Pattern | Description | Eugene Implementation |
|---------|-------------|----------------------|
| **Intent-driven shortcuts** | Detect user intent, surface relevant actions | Trigger words route to agents |
| **In-chat elements** | Rich UI embedded in conversation (tables, buttons) | Web voice UI with inline project cards |
| **Agent-generated UI** | AI decides what interface to show | Future: Eugene generates custom views |
| **Hybrid approach** | Chat + traditional UI coexist | Voice for capture/sort, visual for review |
| **Context preservation** | Actions happen without breaking flow | Sorting happens in conversation |

**Key insight from research:**
> "The future of UI isn't either/or — it's both/and. Chat interfaces that generate structured forms within the conversation."

Eugene's approach: **Voice conversation IS the interface**. The CRT terminal aesthetic reinforces this — you're talking to a computer, not clicking through menus.

---

## Eugene's Unique Positioning

### The Gaps We Fill

| Gap in Market | Eugene's Solution |
|---------------|-------------------|
| Capture requires opening an app | Telegram — already on your phone |
| Categorization requires thinking | Agent suggests, user confirms |
| Review is a chore | Voice-driven sorting ("let's process inbox") |
| Productivity apps are generic | GTD methodology with cost/benefit matrix |
| AI assistants are stateless | PostgreSQL + checkpoints = memory |
| Modern apps are visually bland | Retrofuturism CRT aesthetic |

### The Philosophy

**Things 3** = GTD methodology done right, but requires manual work
**Notion** = Infinite flexibility, but setup paralysis
**Saner.AI** = Voice + AI, but generic productivity
**Linear** = Speed + polish, but team-focused

**Eugene** = GTD + Voice + Agent architecture + Visual delight

### The Tagline

> "State your intent. Eugene handles the rest."

### The Interaction Model

```
TRADITIONAL APP          EUGENE
───────────────          ──────
Open app                 "Hey Eugene..."
Navigate to inbox        (automatic)
Click new task           "...add to braindump:
Fill out form            meeting with Sarah about Q1 planning"
Select project           (agent suggests: project, priority)
Add tags                 (agent extracts: meeting, sarah, q1)
Click save               (automatic)
                         "Got it. Tagged as project planning task."
```

**6 steps → 1 sentence.** That's the disruption.

---

## Design Decisions Informed by Research

### From Things 3
- [x] Temporal buckets (inbox, today, someday, archive)
- [x] Areas for life domain filtering
- [x] Review as first-class feature
- [ ] Consider: recurring task patterns

### From Notion
- [x] Relational data model (inbox ↔ project ↔ journal)
- [x] Multiple views of same data
- [x] Typed properties (status, tags, dates)
- [ ] Consider: formula fields for computed values

### From Saner.AI
- [x] Voice-to-task pipeline
- [x] Morning plan / daily briefing (v1.1)
- [x] Semantic search for journal (v0.2)
- [x] ADHD-friendly defaults (auto-categorize)
- [ ] Consider: email integration

### From Linear
- [x] Speed obsession (<200ms)
- [x] Cmd+K command palette
- [x] Keyboard shortcuts
- [x] Visual polish (retrofuturism theme)
- [x] Opinionated constraints (4 entities only)

### From Multi-Agent Research
- [x] Supervisor pattern (Eugene routes to specialists)
- [x] Human-in-the-loop (user confirms suggestions)
- [x] Role-based agents (capture, inbox, project, journal)
- [ ] Future: agent collaboration on complex requests

### From Conversational UI Research
- [x] Intent-driven routing (trigger words)
- [x] Hybrid approach (voice + visual UI)
- [ ] Future: in-chat rich elements (project cards in conversation)
- [ ] Future: agent-generated adaptive interfaces

---

## Risk Analysis

### Where We Could Fail

| Risk | Mitigation |
|------|------------|
| Voice recognition accuracy | Use proven STT (AssemblyAI), fallback to text |
| Agent hallucination | Conservative extraction, user confirmation |
| Telegram dependency | Web capture as backup, API-first design |
| Retrofuturism is niche | It's a feature, not a bug — attracts our tribe |
| Scope creep | MVP is capture + inbox + projects. Period. |
| Saner.AI already exists | Our edge: Telegram capture, GTD focus, open architecture |

### Where We Have Advantage

| Advantage | Why it matters |
|-----------|----------------|
| No app install for capture | Zero friction beats any feature |
| GTD methodology built-in | Opinionated > flexible for most users |
| Cost/benefit matrix | Strategic view that Saner lacks |
| Open architecture | Self-hostable, customizable |
| LangGraph foundation | Extensible agent system |
| Visual identity | Memorable, differentiated brand |

---

## Next Steps

1. **Validate Telegram capture hypothesis**: Build minimal bot, test with 5 users
2. **Test voice accuracy**: Compare AssemblyAI vs Whisper vs Gemini STT
3. **Prototype CRT UI**: Build one screen with retro-futuristic kit
4. **Define agent prompts**: Write system prompts for each sub-agent
5. **Benchmark Saner.AI**: Sign up, use for 1 week, document gaps

---

## References

| Source | Key Insight |
|--------|-------------|
| Things 3 GTD guides | Areas/Projects/Tags hierarchy |
| Notion database docs | Relations, rollups, views |
| Saner.AI product | Voice-to-task, morning planning |
| Linear philosophy | Speed, keyboard-first, constraints |
| LangGraph supervisor docs | Multi-agent routing pattern |
| CrewAI enterprise adoption | Role-based agent architecture |
| Conversational UI research | Intent-driven, hybrid interfaces |
