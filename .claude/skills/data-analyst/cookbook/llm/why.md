# Why LLM Context Is a Separate Phase

## The Principle

> "Schema is necessary but insufficient. LLMs need semantic context to write correct SQL."

Raw schema (`DESCRIBE TABLE`) tells an LLM the structure. But structure without meaning produces technically valid yet semantically wrong queries. This phase bridges the gap between "what columns exist" and "what they mean in this business."

---

## Why Separate From Validation?

### 1. Different Consumers

**Validation** answers: "Is data quality acceptable for humans?"
**LLM Context** answers: "Can an AI agent reason about this data correctly?"

Humans read documentation differently than LLMs. LLMs need:
- Exhaustive enumeration (not implied context)
- Explicit mappings (term → SQL)
- Anti-patterns as prominently as patterns
- Limits stated as facts, not footnotes

### 2. Different Outputs

Validation produces a **certificate** (pass/fail).
LLM Context produces a **knowledge base** (facts + rules + patterns).

The validation report says "data is clean." The LLM context says "here's how to use it."

### 3. Synthesis Requirement

LLM context requires reading ALL previous phases:
- Business context from `/data-understand`
- Data shape and issues from `/data-explore`
- Transformations applied from `/data-clean`
- Quality metrics from `/data-validate`

No single phase has the complete picture. This phase synthesizes.

---

## The LLM Context Problem

### What Goes Wrong Without It

**User asks**: "Show me unhappy customers"

**Without context, LLM might**:
- Not know "unhappy" maps to NPS detractors (0-6)
- Use INNER JOIN and silently drop 36% of data
- Not mention data coverage limitations
- Query a column that doesn't exist (hallucination)

**With context, LLM will**:
- Map "unhappy" → `nps_score <= 6` (from glossary)
- Use LEFT JOIN to preserve all records (from query patterns)
- State "this covers 64% of SMS surveys" (from limits)
- Only reference real columns (from schema)

### The Information Layers

```
Layer 1: Structure    → "nps_score is INTEGER"
Layer 2: Semantics    → "nps_score is Net Promoter Score, 0-10"
Layer 3: Domain       → "9-10 = promoter, 0-6 = detractor"
Layer 4: Operations   → "always LEFT JOIN to preserve NULLs"
Layer 5: Limits       → "36% of SMS have NULL shop_id"
```

Raw schema gives Layer 1. LLM context gives all 5.

---

## What LLM Context Actually Is

### It IS...

- **A single, comprehensive document** for context injection
- **Schema + semantics** in one place (not separate files)
- **Query recipes** proven to work on THIS data
- **Anti-patterns** that WILL produce wrong results
- **Glossary** mapping business terms to SQL
- **Limits** stated as first-class citizens

### It is NOT...

- **Generic SQL tutorial** (agent already knows SQL)
- **Data dictionary template** (too abstract)
- **Validation report copy** (different purpose)
- **Exhaustive documentation** (focus on agent needs)

---

## The Honest Agent Principle

> "An agent that knows its limits is more useful than one that pretends omniscience."

The LLM context document must enable the agent to:

1. **Answer confidently** when it has the data
2. **Decline honestly** when it doesn't
3. **Caveat appropriately** when coverage is partial

**Good agent response**:
"Here are shops with the most detractors. Note: this only covers 64% of SMS surveys (those linked to shops in our master data). The remaining 36% cannot be grouped by shop."

**Bad agent response**:
"Here are shops with the most detractors." (silently dropped 36% of data)

Honesty requires knowledge of limits. That's what this phase provides.

---

## What This Phase Produces

By the end of `/data-llm`, you should have:

1. **Data Context Document**: `ai-docs/data-llm-{project}.md`
   - TL;DR for quick orientation
   - Schema with semantic annotations
   - Relationship diagram (text-based)
   - Data limits and coverage gaps
   - Query patterns (proven recipes)
   - Anti-patterns (what to avoid)
   - Domain glossary (term → SQL)
   - Temporal boundaries

2. **Agent Readiness**: An LLM can read this one document and:
   - Understand what tables exist and what they mean
   - Know what questions can/cannot be answered
   - Write correct SQL without hallucinating columns
   - Appropriately caveat partial coverage

---

## The Context Injection Pattern

This document is designed for **context injection** into an LLM prompt:

```
System: You are a SQL agent. Here is your data context:

{contents of data-llm-{project}.md}

User: Show me which regions have the most customer complaints.

Agent: [reads context, identifies tables, notes limits, generates SQL, caveats coverage]
```

The document should be:
- **Self-contained**: No external references needed
- **Scannable**: LLM can quickly locate relevant sections
- **Explicit**: No implied context, everything stated
- **Actionable**: Direct term→SQL mappings

---

## Remember

You are not writing documentation for humans. You are writing a knowledge base for an AI agent. The agent cannot ask clarifying questions mid-query. Everything it needs must be in this document.

If the document is incomplete, the agent will hallucinate.
If the limits are hidden, the agent will mislead.
If the glossary is missing, the agent will guess.

Make it complete. Make it explicit. Make it honest.
