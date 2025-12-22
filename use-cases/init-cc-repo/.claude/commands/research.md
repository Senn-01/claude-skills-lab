# Research

Topic: $ARGUMENTS

## Purpose

Deep research phase before implementation. Produces a comprehensive understanding document through structured external knowledge acquisition.

## Philosophy

**Goal-Driven Research with Backpropagation**: Start with the end objective, work backwards to determine what knowledge is needed, then systematically fill gaps using specialized research agents.

```
CONTEXT → GOAL → REQUIREMENTS → GAPS → STRATEGY → EXECUTE → SYNTHESIZE → DOCUMENT
```

This command is for **external knowledge acquisition** (SDKs, libraries, concepts, best practices).
For **internal codebase understanding**, use codebase exploration instead.

---

## Phase 1: Context Gathering

**CRITICAL**: Before any analysis, read mentioned files FULLY.

If the user mentions any files, tickets, or context:
1. Read them completely (no limit/offset parameters)
2. Extract relevant context for the research
3. Note what we already know vs. what we need to learn

Only proceed to Phase 2 after all context is gathered.

---

## Phase 2: Goal Definition (ULTRATHINK)

**IMPORTANT**: Enter extended thinking mode. Take time to deeply reason through this.

Think out loud in a structured scratchpad:

```
═══════════════════════════════════════════════════════════
ULTRATHINK: RESEARCH STRATEGY
═══════════════════════════════════════════════════════════

TOPIC: [What are we researching?]

END STATE VISUALIZATION:
- What does successful research look like?
- What document will we produce?
- What decisions will this enable?
- How will this be used?

BACKPROPAGATION:
- To achieve that end state, what must we understand?
- What are the knowledge domains involved?
- What questions MUST be answered?

CURRENT KNOWLEDGE:
- What do we already know from context?
- What assumptions are we making?
- What's unclear or ambiguous?

KNOWLEDGE GAPS:
- Gap 1: [description] → Why critical?
- Gap 2: [description] → Why critical?
- ...

RESEARCH APPROACH:
- Which gaps need official docs? (Context7)
- Which gaps need ecosystem wisdom? (Tavily)
- Which gaps need real-world examples? (Tavily)
- Any codebase scanning needed?

═══════════════════════════════════════════════════════════
```

---

## Phase 3: Design Research Strategy

### Specialized Research Agents

Map each knowledge gap to a specialized researcher:

| Agent Type | Role | Tool | When to Use |
|------------|------|------|-------------|
| **Concept Researcher** | Understand what something IS | Tavily | New/unfamiliar topics |
| **Docs Researcher** | Official documentation deep-dive | Context7 | Library APIs, usage patterns |
| **Examples Researcher** | Real-world usage patterns | Tavily | Implementation patterns, tutorials |
| **Ecosystem Researcher** | Community wisdom, best practices | Tavily | Trade-offs, alternatives, gotchas |
| **Codebase Scanner** | How our code relates | Glob/Grep | Integration points (optional) |

### Design Queries

For each gap, design specific queries:
- Make queries precise and searchable
- Pair each query with the gap it fills
- Assign to appropriate researcher type
- Group related queries for parallel execution

### Determine Research Depth

```
QUICK RESEARCH (≤3 queries, single domain):
→ Execute immediately, show results

DEEP RESEARCH (>3 queries OR multiple domains OR user says "deep"):
→ Present strategy for approval first
```

---

## Phase 4: Present Strategy for Approval

**If DEEP RESEARCH**, present and wait for approval:

```markdown
## Research Strategy

**Goal**: [end state in one sentence]

**Knowledge Gaps Identified**:
1. [Gap] - [why critical]
2. ...

**Research Plan**:

| # | Query | Researcher | Tool | Fills Gap |
|---|-------|------------|------|-----------|
| 1 | "..." | Concept | Tavily | [gap] |
| 2 | "..." | Docs | Context7 | [gap] |
| 3 | "..." | Examples | Tavily | [gap] |
| ... |

**Agent Structure**:
- **Concept Researcher**: Queries 1, 2 → Understand fundamentals
- **Docs Researcher**: Queries 3, 4 → API surface, official patterns
- **Examples Researcher**: Queries 5, 6 → Real-world usage
- **Ecosystem Researcher**: Query 7 → Best practices, trade-offs

**Estimated**: [X] queries across [Y] agents

Proceed with research?
```

Wait for user approval before executing.

---

## Phase 5: Execute Research (Parallel)

Spawn specialized agents in parallel using the Task tool.

### Agent Prompt Templates

**Concept Researcher**:
```
You are a CONCEPT RESEARCHER. Your role is to understand what something IS.

Topic: [specific concept]
Queries:
1. [query]
2. [query]

Use mcp__tavily__tavily-search with:
- search_depth: "basic"
- max_results: 5

Return format:
## Concept: [Name]

### Definition
[What is this? Core mental model]

### Key Components
- Component 1: [description]
- ...

### How It Relates To
- [Related concept]: [relationship]

### Sources
- [url]: [what it provided]
```

**Docs Researcher**:
```
You are a DOCS RESEARCHER. Your role is to extract official documentation.

Library: [library name]
Focus: [specific area]

Steps:
1. Use mcp__context7__resolve-library-id to find the library
2. Use mcp__context7__get-library-docs with topic parameter

Return format:
## Documentation: [Library]

### API Surface
- [Function/Method]: [what it does]
- ...

### Official Usage Pattern
[code example from docs]

### Configuration Options
- [option]: [description]

### Sources
- Context7 library: [library-id]
```

**Examples Researcher**:
```
You are an EXAMPLES RESEARCHER. Your role is to find real-world usage.

Topic: [what to find examples of]
Queries:
1. [query]

Use mcp__tavily__tavily-search with:
- search_depth: "basic"
- max_results: 8
- include_domains: ["github.com", "dev.to", "medium.com"] (if relevant)

Return format:
## Examples: [Topic]

### Pattern 1: [Name]
[description]
[code snippet if found]
Source: [url]

### Pattern 2: [Name]
...

### Common Gotchas
- [gotcha]: [how to avoid]

### Sources
- [url]: [what it provided]
```

**Ecosystem Researcher**:
```
You are an ECOSYSTEM RESEARCHER. Your role is to gather community wisdom.

Topic: [what to research]
Queries:
1. [query about best practices]
2. [query about alternatives/trade-offs]

Use mcp__tavily__tavily-search with:
- search_depth: "advanced" (for comprehensive results)
- max_results: 10

Return format:
## Ecosystem: [Topic]

### Best Practices
- [practice]: [why]
- ...

### Common Mistakes
- [mistake]: [consequence]

### Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| [A] | ... | ... |

### Community Sentiment
[What does the community think? Recent trends?]

### Sources
- [url]: [what it provided]
```

### Execution Rules

1. **Spawn all agents in parallel** (single message, multiple Task tool calls)
2. **WAIT FOR ALL agents to complete** before proceeding
3. **Track all queries executed** and their results

---

## Phase 6: Synthesize

After ALL agents complete, synthesize findings:

1. **Compile** all agent outputs
2. **Identify patterns** across findings
3. **Note contradictions** or conflicting information
4. **Highlight critical insights** that affect decisions
5. **Flag remaining unknowns** that couldn't be resolved
6. **Connect to our context** - how does this apply to us?

---

## Phase 7: Document

Write comprehensive research document to `ai-docs/research-{topic-slug}.md`:

```markdown
---
topic: "[Research Topic]"
date: [YYYY-MM-DDTHH:MM:SSZ]
status: complete
tools_used: [tavily, context7]
queries_executed: [number]
agents_spawned: [number]
---

# Research: [Topic]

## Executive Summary

[2-3 sentences: what we learned, the key insight, what decisions this enables]

## Research Goal

[What this research aimed to achieve, what questions it answers]

## Concept Overview

[What IS this thing? Mental model, key terminology]

## How It Works

[Mechanics, architecture, key components, data flow]

## Best Practices

[Ecosystem wisdom, recommended patterns, what experts say]

### Do
- [practice]: [why]

### Don't
- [anti-pattern]: [consequence]

## Integration Considerations

[How this fits our context, what we'd need to do, dependencies]

## Decision Points

Based on this research, we can now decide:
1. [Decision 1]: [options and recommendation]
2. [Decision 2]: [options and recommendation]

## Alternatives Considered

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| [A] | ... | ... | [chosen/rejected + why] |

## Sources

| Source | Type | What It Provided |
|--------|------|------------------|
| [url] | Docs | [insight] |
| [url] | Article | [insight] |

## Queries Executed

| Query | Tool | Agent | Result |
|-------|------|-------|--------|
| "..." | Tavily | Concept | [brief result] |
| "..." | Context7 | Docs | [brief result] |

## Open Questions

[What remains unclear, potential follow-up research needed]

## Follow-up Research

[Leave empty - will be appended if user asks more questions]
```

---

## Phase 8: Report

Output summary to user:

```
═══════════════════════════════════════════════════════════
✓ RESEARCH COMPLETE: [topic]
═══════════════════════════════════════════════════════════

Document: ai-docs/research-{slug}.md

Key Findings:
• [Finding 1]
• [Finding 2]
• [Finding 3]

Decision Points Ready:
• [Decision 1]
• [Decision 2]

Ready for: [next phase - planning/implementation/more research]

Questions? Ask and I'll append to the research doc.
═══════════════════════════════════════════════════════════
```

---

## Phase 9: Handle Follow-ups

If user has follow-up questions:

1. **Do NOT create new document** - append to existing
2. Add new section: `## Follow-up: [Question] ([timestamp])`
3. Spawn additional agents as needed
4. Update frontmatter: add `last_updated: [date]`
5. Synthesize new findings with existing research

---

## Tool Reference

| Tool | Use For | Cost |
|------|---------|------|
| `mcp__tavily__tavily-search` | Web research | 1 credit (basic), 2 credits (advanced) |
| `mcp__context7__resolve-library-id` | Find library ID | - |
| `mcp__context7__get-library-docs` | Official docs | - |

**Tavily Parameters**:
- `search_depth`: "basic" (fast) or "advanced" (comprehensive)
- `max_results`: 5-10 for focused, 10-15 for broad
- `include_domains`: Restrict to authoritative sources
- `topic`: "general" or "news"

**Context7 Parameters**:
- Always `resolve-library-id` first to get valid ID
- `topic`: Focus on specific area (e.g., "hooks", "authentication")
- `mode`: "code" for APIs, "info" for concepts

---

## Rules

1. **Read context FIRST** - never analyze without reading mentioned files
2. **ULTRATHINK the strategy** - deep reasoning before designing queries
3. **Approval for deep research** - show strategy if >3 queries
4. **Parallel execution** - spawn all agents in single message
5. **WAIT FOR ALL** - never synthesize with partial results
6. **Source everything** - every finding needs attribution
7. **Track queries** - record what was searched and found
8. **Append follow-ups** - one doc per topic, iterate on it
9. **No implementation** - research phase produces understanding, not code
