---
title: "Scratchpad: Orange cx intelligence agent"
client: Orange Belgium
version: 0.1.0
phase: Discovery
principles:
  - Cautious progression
  - Simplicity first
  - No over-engineering
changelog:
  - version: 0.1.0
    date: 2025-12-22
    changes:
      - Initial creation
---

# Orange cx intelligence agent — Discovery Scratchpad

---

## 0. Context for Future Reference

### Client
**Orange Belgium** is a major telecommunications provider offering mobile, internet, and TV services. They operate a network of ~100 physical retail shops ("Orange Shops") where customers can purchase products, activate services, and get support.

### Key Stakeholders
- **Astrid / Aurore**: Management contacts who commissioned this project
- **District/KAM Managers**: Regional managers overseeing groups of shops
- **Shop Advisors**: Frontline staff at individual shops

### User (Dev-0)
The developer working on this project specializes in system prompt engineering and building agentic workflows on the Nexus platform. This is a consulting engagement to build an internal analytics tool.

### Platform
**Nexus** is a low-code AI agent platform that enables building sophisticated conversational agents through modular architecture. Key capabilities:
- Main AI agent with system prompt + skills + knowledge access
- Workflows with HITL (Human-in-the-Loop) nodes for data collection
- Plugin integrations (including BigQuery)
- AI Tasks for specialized sub-processing
- Template population for document generation (PPTX/PDF)

See project files for Nexus documentation: `NEXUS_PLATFORM_ARCHITECTURE_v2_1.md`, `nexus-system-prompt-template-v3.md`

### Existing System
There is a **separate existing workflow** that automatically responds to Google Reviews. This feedback analysis agent is intentionally standalone — it analyzes feedback but does NOT respond to reviews.

### Terminology Glossary

| Term | Meaning |
|------|---------|
| **MOBIS code** / **Aramis code** | Orange's internal shop identifier (e.g., "MOBIS519"). Used interchangeably. Format: "MOBIS" + 3 digits. |
| **Verbatim** | Free-text customer comment (as opposed to numeric score) |
| **KAM** | Key Account Manager — regional manager overseeing multiple shops |
| **Orange Shop** | Orange-branded retail location (vs. third-party distributors) |
| **SMS/Survey** | Post-transaction satisfaction survey sent via SMS |
| **Macro-Segment** | Shop classification in Full Shop Infos (e.g., "Orange Shops", "DISTRIBUTORS", "CLOSED") |

---

## 1. Purpose

Enable Orange Belgium management and shop teams to query customer feedback data conversationally, extract actionable insights, and generate presentation-ready reports.

---

## 2. Problem Statement

The sales team cannot objectively communicate customer insights to frontline shop staff:

- Feedback data exists but sits unanalyzed in spreadsheets
- Assertions feel like management opinion, not customer reality
- No systematic way to quantify and prioritize improvement areas

**Core Insight**: This agent serves a political function. "The customer says X" carries more weight than "management says X." The agent provides external authority for change management.

---

## 3. Solution Overview

An AI agent that:

1. Accepts natural language queries ("Top 5 complaints for shop X in November")
2. Filters and retrieves relevant feedback via BigQuery
3. Extracts themes and sentiment from verbatims
4. Quantifies results ("32 eSIM complaints out of 500 total reviews")
5. Generates PPTX/PDF reports for stakeholders

---

## 4. Scope Definition

### In Scope

| Capability | Description |
|------------|-------------|
| Natural language queries | Interpret user intent, filter data accordingly |
| Data aggregation | Combine Google Reviews + SMS/Survey sources |
| Time filtering | Week, month, quarter, custom ranges |
| Shop filtering | Single shop, region, all Orange Shops |
| Theme extraction | LLM-prompted categorization of verbatims |
| Quantification | Counts, percentages, ratios with denominators |
| Shop comparison | Rankings, best/worst performers |



## 5. Example Queries (Requirements)

### Management Queries
- "What improvements should we prioritize based on complaint volume by theme?"
- "Top 5 improvement points across shops for the last 3 months"
- "Analyze the best-performing shop — what positive things are customers saying?"

**Output expectation**: "X cases about eSIM out of Y total reviews" (denominators required)

### District/Shop Queries
- "How did shop X perform in November? What needs attention and what's going well?"
- "What did customers say about my shop last week — positives and negatives?"
- "What actions can I take at my level to improve customer experience?"

### Implied Capabilities
- Time filtering (week, month, quarter, custom)
- Shop filtering (single, district, all)
- Theme extraction (LLM-prompted)
- Quantified outputs (counts, percentages, ratios)
- Ranking/comparison
- Report generation (PPTX/PDF)

---

