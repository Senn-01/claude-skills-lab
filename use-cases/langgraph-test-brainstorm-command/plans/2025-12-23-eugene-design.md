---
description: Eugene - Voice-first GTD command center with LangGraph supervisor routing multimodal captures to structured inbox, projects, and journal
version: 0.3.0
status: design
created: 2025-12-23
changelog:
  - version: 0.3.0
    date: 2025-12-23
    changes:
      - Refined project philosophy (strategic commitment model)
      - Added category taxonomy (WORK/LEARN/BUILD/MANAGE)
      - Added priority, due_date, mandatory fields
      - Added why and done_looks_like for clarity
      - Documented post-MVP urgency visualization vision
  - version: 0.2.0
    date: 2025-12-23
    changes:
      - Added competitive analysis (Things 3, Notion, Saner.AI, Linear)
      - Defined unique positioning and differentiators
      - Added design decisions informed by research
      - Clarified agent-as-interface philosophy
  - version: 0.1.0
    date: 2025-12-23
    changes:
      - Initial design document
      - Core architecture defined (supervisor pattern)
      - Data model specified (inbox, project, journal, trends)
      - Voice pipeline designed (STT → Agent → TTS)
      - Tech stack selected (FastAPI, LangGraph, PostgreSQL, React)
linked_files:
  - docs/plans/2025-12-23-eugene-competitive-analysis.md
---

# Eugene: Personal Command Center

## Problem

**Capture chaos.** Ideas and tasks scatter across voice memos, screenshots, notes apps, and mental stack. No single inbox. No processing workflow. Items disappear.

## Solution

**Eugene** = voice-first AI agent that acts as universal capture inbox. Multimodal input (voice, image, link, text) converts to structured data. User sorts during review. Projects surface on cost/benefit matrix.

## Core Concept

```
CAPTURE → PROCESS → STORE → SORT → ACT
   │          │        │       │      │
 voice     Gemini    Postgres  user   projects
 image     Flash 3.0  inbox   review  matrix
 link      extract            voice   journal
 text      categorize         or web
```

**Two interfaces, one brain:**

| Interface | Purpose | Platform |
|-----------|---------|----------|
| Telegram Bot | Capture on-the-go | Mobile |
| Web Command Center | Review, sort, strategize | Desktop |

Both share the same backend. Both support voice-first interaction.

---

## Architecture

### System Overview

```
┌─────────────────┐         ┌─────────────────────────────────┐
│  Telegram Bot   │         │      Web Command Center         │
│                 │         │                                 │
│  Voice/Img/Text │         │  Voice input + Retro-futuristic │
│  via Telegram   │         │  CRT terminal UI                │
│  native support │         │                                 │
└────────┬────────┘         └───────────────┬─────────────────┘
         │                                  │
         │         ┌────────────────────────┴────────┐
         │         │                                 │
         │         ▼                                 ▼
         │    ┌─────────┐    ┌─────────┐    ┌─────────┐
         │    │   STT   │───▶│  Agent  │───▶│   TTS   │
         │    │Assembly │    │LangGraph│    │Cartesia │
         │    └─────────┘    └────┬────┘    └─────────┘
         │                        │
         └────────────────────────┤
                                  ▼
                        ┌───────────────────┐
                        │     FastAPI       │
                        │                   │
                        │  CRUD endpoints   │
                        │  for all entities │
                        └─────────┬─────────┘
                                  │
                                  ▼
                        ┌───────────────────┐
                        │    PostgreSQL     │
                        │                   │
                        │  inbox_items      │
                        │  projects         │
                        │  journal_notes    │
                        │  trend_events     │
                        └───────────────────┘
```

### Voice Pipeline (Web)

Async generator pattern from LangChain voice-sandwich-demo:

```python
async def voice_pipeline(audio_stream):
    async for transcript in stt_stage(audio_stream):      # AssemblyAI
        async for agent_event in agent_stage(transcript): # LangGraph
            async for audio_chunk in tts_stage(agent_event):  # Cartesia
                yield audio_chunk
```

**Properties:**
- Streaming (no wait for full transcript)
- Interruptible (user can cut off mid-response)
- Modular (swap any stage independently)

### Multi-Agent Architecture (LangGraph Supervisor)

Eugene = supervisor agent. Routes to specialized sub-agents.

```
                              ┌─────────────────────┐
                              │       EUGENE        │
                              │    (Supervisor)     │
                              │                     │
                              │  1. Parse input     │
                              │  2. Classify intent │
                              │  3. Route to agent  │
                              │  4. Return response │
                              └──────────┬──────────┘
                                         │
           ┌─────────────┬───────────────┼───────────────┬─────────────┐
           ▼             ▼               ▼               ▼             ▼
    ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
    │  CAPTURE   │ │   INBOX    │ │  PROJECT   │ │  JOURNAL   │ │  [FUTURE]  │
    │   AGENT    │ │   AGENT    │ │   AGENT    │ │   AGENT    │ │            │
    └────────────┘ └────────────┘ └────────────┘ └────────────┘ └────────────┘
```

**Agent responsibilities:**

| Agent | Trigger phrases | Actions |
|-------|-----------------|---------|
| CAPTURE | "braindump", "add", "capture" | Multimodal → text, extract metadata, store inbox item |
| INBOX | "process inbox", "what's in inbox", "sort" | List items, interactive sorting, assign to project |
| PROJECT | "create project", "show projects", "update" | CRUD projects, cost/benefit scoring |
| JOURNAL | "add to journal", "note that", "search journal" | Create notes with YAML frontmatter, semantic search |

**Scalability:** Add new agent = add node to graph + update supervisor routing. No architecture rewrite.

---

## Data Model

### inbox_item

Captures all incoming data before user sorts.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| raw_input | TEXT | Original voice transcript / image description / link / text |
| processed_text | TEXT | Cleaned, extracted UTF-8 content |
| source | ENUM | `telegram`, `web` |
| input_type | ENUM | `voice`, `image`, `link`, `text` |
| suggested_type | ENUM | `task`, `idea`, `reference`, `project` (agent guess) |
| suggested_tags | TEXT[] | Agent-extracted tags |
| status | ENUM | `inbox`, `processed`, `archived` |
| project_id | UUID? | FK to project (if assigned) |
| created_at | TIMESTAMP | Capture timestamp |

### project

User-promoted items for strategic tracking and prioritization.

**Philosophy:** A project is a conscious commitment to invest limited resources toward a specific outcome, classified by life domain, and evaluated by cost/benefit ratio.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | TEXT | Project title |
| description | TEXT | Project details |
| why | TEXT | One sentence: why this matters |
| done_looks_like | TEXT | Completion criteria |
| category | ENUM | `WORK`, `LEARN`, `BUILD`, `MANAGE` (life domain) |
| tags | TEXT[] | Flexible cross-cutting labels |
| cost | INT (1-5) | Effort/complexity score |
| benefit | INT (1-5) | Value/impact score |
| priority | ENUM | `P0`, `P1`, `P2`, `P3` (urgency × importance) |
| due_date | DATE? | Hard deadline (NULL = no deadline) |
| mandatory | BOOLEAN | Can't drop even if ROI is bad |
| status | ENUM | `active`, `someday`, `done`, `dropped` |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last modification |

**Categories (Life Domains):**

| Category | Purpose | Example |
|----------|---------|---------|
| WORK | Professional obligations | Client deliverables, reports |
| LEARN | Skill development | Courses, books, certifications |
| BUILD | Creative output | Side projects, apps, art |
| MANAGE | Life administration | Health, finance, admin |

**Cost/Benefit Matrix:** Projects plotted by strategic value. X-axis = cost, Y-axis = benefit.

```
         HIGH BENEFIT
              │
    QUICK     │    MAJOR
    WINS      │    PROJECTS
              │
──────────────┼──────────────
              │
    FILL      │    RECONSIDER
    TIME      │
              │
         LOW BENEFIT

       LOW COST ──────── HIGH COST
```

**Post-MVP Vision (Urgency Visualization):**
- 🔴 Pulsing indicator when due date approaches
- ⚡ Glow effect for high priority (P0/P1)
- 🔒 Badge for mandatory projects
- Visual urgency overlays on matrix without cluttering strategic view

### journal_note

Reflective notes with structured metadata for retrieval.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| title | TEXT | Note title |
| content | TEXT | Markdown body |
| frontmatter | JSONB | Structured metadata (see below) |
| embedding | VECTOR(1536) | Semantic search vector |
| created_at | TIMESTAMP | Creation timestamp |

**Frontmatter schema:**

```yaml
tags: [reflection, burnout, win]
mood: contemplative
energy: 3
linked_items:
  - inbox_item_id: uuid
  - project_id: uuid
```

### trend_event

Activity log for analytics and pattern detection.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| event_type | ENUM | `capture`, `sort`, `project_created`, `journal_entry` |
| metadata | JSONB | Flexible payload (source, tags, counts) |
| created_at | TIMESTAMP | Event timestamp |

**Query examples:**
- "Captures per day this week" → count by date
- "Most common tags" → aggregate metadata.tags
- "Capture source distribution" → group by metadata.source

---

## Tech Stack

### Backend

| Component | Technology | Rationale |
|-----------|------------|-----------|
| API | FastAPI | Python, async, Pydantic types, auto-docs |
| Agent framework | LangGraph | Supervisor pattern, human-in-loop, checkpoints |
| Database | PostgreSQL | JSONB for flexible metadata, pgvector for embeddings |
| Multimodal | Gemini Flash 3.0 | Fast, cheap, voice+image→text |
| STT | AssemblyAI | Real-time streaming transcription |
| TTS | Cartesia | Low-latency voice synthesis |
| Deployment | Railway or Fly.io | Easy Python deploys, managed Postgres |

### Frontend (Web)

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Framework | React 18 + TypeScript | Matches retro-futuristic UI kit |
| Build | Vite | Fast, used by UI kit |
| Routing | React Router DOM 6 | Already UI kit dependency |
| API client | TanStack Query | Caching, loading states |
| State | Zustand | Lightweight, no boilerplate |
| Styling | UI kit CSS + Tailwind | Retro components + layout utilities |
| Voice | Web Speech API + WebSocket | Browser-native mic, streaming to backend |

**UI Kit:** [Imetomi/retro-futuristic-ui-design](https://github.com/Imetomi/retro-futuristic-ui-design) — CRT terminal aesthetic, Cassette Futurism style.

### Mobile (Capture)

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Interface | Telegram Bot | Zero app development, native voice/image/file support |
| Webhook | FastAPI endpoint | Receives Telegram updates, triggers agent |

---

## API Endpoints

### Inbox

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/inbox` | Create inbox item (from agent) |
| GET | `/inbox` | List inbox items (filterable by status) |
| GET | `/inbox/{id}` | Get single inbox item |
| PATCH | `/inbox/{id}` | Update item (status, project_id, tags) |
| DELETE | `/inbox/{id}` | Archive/delete item |

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/projects` | Create project |
| GET | `/projects` | List projects (filterable by status) |
| GET | `/projects/{id}` | Get single project with linked items |
| PATCH | `/projects/{id}` | Update project (name, cost, benefit, status) |
| DELETE | `/projects/{id}` | Drop project |

### Journal

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/journal` | Create note |
| GET | `/journal` | List notes (paginated) |
| GET | `/journal/search?q=` | Semantic search via embeddings |
| GET | `/journal/{id}` | Get single note |
| PATCH | `/journal/{id}` | Update note |

### Trends

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/trends/captures` | Capture count by day/week/month |
| GET | `/trends/tags` | Tag frequency distribution |
| GET | `/trends/sources` | Capture source breakdown |

### Voice (WebSocket)

| Endpoint | Description |
|----------|-------------|
| `ws://host/voice` | Bidirectional audio stream (mic in, TTS out) |

---

## Agent Intent Classification

Eugene supervisor classifies user intent before routing.

### Trigger Word Matrix

| Pattern | Intent | Route to |
|---------|--------|----------|
| "hey eugene, braindump..." | quick_capture | CAPTURE (minimal processing) |
| "add to inbox", "capture this" | smart_capture | CAPTURE (extract metadata) |
| "what's in my inbox", "show inbox" | list_inbox | INBOX |
| "let's process inbox", "sort my items" | sort_inbox | INBOX (interactive loop) |
| "create project", "new project called" | create_project | PROJECT |
| "show projects", "project status" | list_projects | PROJECT |
| "add to journal", "note that" | create_journal | JOURNAL |
| "search journal for", "find notes about" | search_journal | JOURNAL |

### Default Behavior

No trigger word detected → smart_capture. Agent extracts:
- Title (first sentence or summary)
- Type (task/idea/reference/project)
- Tags (keywords, entities)

User always has final authority during inbox review.

---

## User Flows

### Flow 1: Mobile Capture (Telegram)

```
User                          Telegram                    Eugene
  │                              │                          │
  │ Voice: "Remember to call     │                          │
  │ dentist about appointment"   │                          │
  │ ─────────────────────────────▶                          │
  │                              │  POST /telegram/webhook  │
  │                              │ ─────────────────────────▶
  │                              │                          │
  │                              │      CAPTURE agent:      │
  │                              │      - Transcribe        │
  │                              │      - Extract: task,    │
  │                              │        [health, call]    │
  │                              │      - Store inbox       │
  │                              │                          │
  │                              │ ◀───────────────────────│
  │ ◀─────────────────────────── │                          │
  │ "Got it. Tagged as task:     │                          │
  │  health, call. In your       │                          │
  │  inbox."                     │                          │
```

### Flow 2: Web Inbox Processing (Voice)

```
User                          Web App                     Eugene
  │                              │                          │
  │ "Hey Eugene, let's process   │                          │
  │  my inbox"                   │                          │
  │ ─────────────────────────────▶                          │
  │                              │  ws://voice stream       │
  │                              │ ─────────────────────────▶
  │                              │                          │
  │                              │      INBOX agent:        │
  │                              │      - Fetch inbox items │
  │                              │      - Start sort loop   │
  │                              │                          │
  │ ◀───────────────────────────────────────────────────────│
  │ [TTS] "You have 8 items.     │                          │
  │  First: 'Call dentist'.      │                          │
  │  Task about health.          │                          │
  │  Keep, project, or trash?"   │                          │
  │                              │                          │
  │ "Make it a project,          │                          │
  │  low effort, medium value"   │                          │
  │ ─────────────────────────────▶                          │
  │                              │      PROJECT agent:      │
  │                              │      - Create project    │
  │                              │        cost=2, benefit=3 │
  │                              │      - Link inbox item   │
  │                              │      - Continue loop     │
  │                              │                          │
  │ ◀───────────────────────────────────────────────────────│
  │ [TTS] "Created project       │                          │
  │  'Call dentist'. Next item..." │                        │
```

### Flow 3: Journal Entry

```
User                          Eugene
  │                              │
  │ "Eugene, add to journal:     │
  │  Today I realized I spend    │
  │  too much time on low-value  │
  │  tasks. Need to protect      │
  │  deep work time."            │
  │ ─────────────────────────────▶
  │                              │
  │                              │  JOURNAL agent:
  │                              │  - Extract title: "Protect deep work time"
  │                              │  - Extract tags: [productivity, reflection]
  │                              │  - Infer mood: contemplative
  │                              │  - Generate embedding
  │                              │  - Store note
  │                              │
  │ ◀─────────────────────────────
  │ "Saved to journal: 'Protect  │
  │  deep work time'. Tagged     │
  │  productivity, reflection."  │
```

---

## MVP Scope

### Included (v0.1)

| Feature | Priority | Notes |
|---------|----------|-------|
| Telegram bot capture | P0 | Voice, image, text |
| Multimodal → text (Gemini) | P0 | Core processing |
| Smart categorization | P0 | Extract title, type, tags |
| PostgreSQL inbox storage | P0 | Structured data |
| FastAPI CRUD endpoints | P0 | All entities |
| Web app inbox view | P0 | List, manual sort |
| Web app project list | P0 | Simple list view |
| Web app trends (basic) | P1 | Capture count chart |
| LangGraph supervisor | P0 | Routing architecture |

### Excluded (Post-MVP)

| Feature | Target Version | Notes |
|---------|----------------|-------|
| Voice on web (full pipeline) | v0.2 | STT → Agent → TTS |
| Cost/benefit matrix view | v0.2 | Strategic project visualization |
| Journal agent + semantic search | v0.2 | Embeddings, retrieval |
| Urgency visualization | v0.3 | Pulsing due dates, priority glow |
| Time tracking | v0.3 | Start/stop timer, log time per project |
| Time-boxing / scheduling | v0.3 | Block time for projects |
| macOS reminders integration | v0.3 | osascript alarms |
| Push to external tools (Notion, Todoist) | v0.4 | Sync selected items |
| Advanced analytics | v0.4 | Trends, patterns, insights |

---

## Directory Structure

```
eugene/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry
│   │   ├── api/
│   │   │   ├── inbox.py         # Inbox endpoints
│   │   │   ├── projects.py      # Project endpoints
│   │   │   ├── journal.py       # Journal endpoints
│   │   │   ├── trends.py        # Analytics endpoints
│   │   │   └── telegram.py      # Telegram webhook
│   │   ├── agents/
│   │   │   ├── supervisor.py    # Eugene supervisor
│   │   │   ├── capture.py       # Capture agent
│   │   │   ├── inbox.py         # Inbox agent
│   │   │   ├── project.py       # Project agent
│   │   │   └── journal.py       # Journal agent
│   │   ├── models/
│   │   │   ├── inbox.py         # Pydantic + SQLAlchemy
│   │   │   ├── project.py
│   │   │   ├── journal.py
│   │   │   └── trend.py
│   │   ├── services/
│   │   │   ├── multimodal.py    # Gemini Flash integration
│   │   │   ├── stt.py           # AssemblyAI
│   │   │   └── tts.py           # Cartesia
│   │   └── db/
│   │       ├── database.py      # Connection
│   │       └── migrations/      # Alembic
│   ├── pyproject.toml
│   └── uv.lock
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CRTTerminal.tsx  # From retro-futuristic-ui
│   │   │   ├── Inbox.tsx
│   │   │   ├── Projects.tsx
│   │   │   ├── Trends.tsx
│   │   │   └── VoiceInput.tsx
│   │   ├── hooks/
│   │   │   ├── useVoice.ts      # WebSocket + mic
│   │   │   └── useApi.ts        # TanStack Query
│   │   ├── stores/
│   │   │   └── app.ts           # Zustand
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── docs/
│   └── plans/
│       └── 2025-12-23-eugene-design.md
└── README.md
```

---

## Implementation Order

Execute in sequence. Each phase delivers working functionality.

### Phase 1: Backend Foundation

1. Initialize FastAPI project with UV
2. Configure PostgreSQL with SQLAlchemy
3. Create data models (inbox, project, trend_event)
4. Implement CRUD endpoints for inbox
5. Set up Alembic migrations

**Deliverable:** API that stores and retrieves inbox items.

### Phase 2: Telegram Capture

1. Create Telegram bot via BotFather
2. Implement webhook endpoint
3. Integrate Gemini Flash for voice→text
4. Build CAPTURE agent (basic extraction)
5. Connect agent to inbox storage

**Deliverable:** Voice messages in Telegram create inbox items.

### Phase 3: LangGraph Supervisor

1. Define graph state schema
2. Implement supervisor node (intent classification)
3. Create CAPTURE, INBOX, PROJECT agent nodes
4. Wire routing edges
5. Add human-in-loop checkpoints

**Deliverable:** Eugene routes intents to correct agents.

### Phase 4: Web Frontend

1. Initialize React + Vite + TypeScript
2. Integrate retro-futuristic UI components
3. Build Inbox view with TanStack Query
4. Build Projects view
5. Add basic Trends chart

**Deliverable:** Web dashboard shows inbox and projects.

### Phase 5: Voice on Web

1. Implement WebSocket endpoint for voice
2. Integrate AssemblyAI STT (streaming)
3. Integrate Cartesia TTS
4. Connect voice pipeline to supervisor
5. Build VoiceInput component

**Deliverable:** Voice conversations in web app.

---

## Success Criteria

### MVP Launch (v0.1)

| Criterion | Measurement |
|-----------|-------------|
| Capture works | Voice message in Telegram creates inbox item in <5s |
| Categorization useful | >70% of suggested tags are relevant |
| Web shows data | Inbox and projects render correctly |
| No data loss | All captures persisted to PostgreSQL |

### Product-Market Fit (v1.0)

| Criterion | Measurement |
|-----------|-------------|
| Daily active use | User captures >5 items/day for 2 weeks |
| Processing habit | User processes inbox >2x/week |
| Project tracking | >3 active projects with cost/benefit scores |
| Voice preference | >50% of interactions via voice |

---

## Open Questions

| Question | Impact | Decision Needed By |
|----------|--------|-------------------|
| AssemblyAI vs Whisper vs Gemini for STT? | Cost, latency, accuracy | Phase 2 |
| Cartesia vs ElevenLabs for TTS? | Voice quality, cost | Phase 5 |
| pgvector vs Pinecone for embeddings? | Complexity, cost | Phase 6 (journal) |
| Self-host vs Railway vs Fly.io? | Cost, ops burden | Phase 1 |
| Telegram only or also WhatsApp? | User reach | Post-MVP |

---

## Competitive Positioning

See full analysis: `docs/plans/2025-12-23-eugene-competitive-analysis.md`

### Philosophy

> "Software-as-a-Service platforms that force users to click through slow UIs will be disrupted by agents that interact with the database/API directly."

> "The best UIs will become prompt interfaces where the user states an intent, and a swarm of agents executes the CRUD operations in the background."

### What We Learn From

| Product | Key Lesson | Eugene Implementation |
|---------|------------|----------------------|
| **Things 3** | GTD methodology, temporal buckets, review ritual | Inbox → Today → Someday → Archive flow |
| **Notion** | Relational data, multiple views, typed properties | Inbox ↔ Project ↔ Journal relations |
| **Saner.AI** | Voice-to-task, morning planning, ADHD-friendly | Voice capture, agent suggestions, minimal UI |
| **Linear** | Speed obsession, keyboard-first, visual polish | <200ms interactions, Cmd+K, retrofuturism |

### Our Unique Edge

| Gap in Market | Eugene's Solution |
|---------------|-------------------|
| Capture requires opening an app | Telegram — already on your phone |
| Categorization requires thinking | Agent suggests, user confirms |
| Review is a chore | Voice-driven sorting |
| Productivity apps are generic | GTD + cost/benefit matrix |
| AI assistants are stateless | PostgreSQL + checkpoints = memory |
| Modern apps are visually bland | Retrofuturism CRT aesthetic |

### The Tagline

> **"State your intent. Eugene handles the rest."**

### The Disruption

```
TRADITIONAL APP          EUGENE
───────────────          ──────
Open app                 "Hey Eugene..."
Navigate to inbox        (automatic)
Click new task           "...add to braindump:
Fill out form            meeting with Sarah about Q1"
Select project           (agent suggests)
Add tags                 (agent extracts)
Click save               (automatic)
───────────────          ──────
6 steps                  1 sentence
```

---

## References

| Resource | URL |
|----------|-----|
| LangGraph docs | https://docs.langchain.com/oss/python/langgraph/overview |
| LangGraph supervisor pattern | https://docs.langchain.com/oss/python/langchain/multi-agent/subagents-personal-assistant |
| Voice Sandwich Demo | https://github.com/langchain-ai/voice-sandwich-demo |
| Retro-futuristic UI | https://github.com/Imetomi/retro-futuristic-ui-design |
| FastAPI | https://fastapi.tiangolo.com |
| TanStack Query | https://tanstack.com/query |
| Telegram Bot API | https://core.telegram.org/bots/api |
| Things 3 GTD Guide | https://culturedcode.com/things/guide/ |
| Notion Database Docs | https://www.notion.com/help/database-properties |
| Saner.AI | https://www.saner.ai |
| Linear App | https://linear.app |
