---
topic: "LLM-Readable Markdown Design Patterns"
date: 2025-12-19T00:00:00Z
updated: 2025-12-19T00:00:00Z
status: complete
tools_used: [tavily, context7]
queries_executed: 6
agents_spawned: 3
rationale: |
  Research to inform creation of a /md command for generating LLM-optimized
  markdown files. User template requires YAML frontmatter (rationale, changelog,
  linked files), IDKW style, and logical structure for thinking LLM consumption.
changelog:
  - version: "0.1.1"
    date: 2025-12-19
    changes:
      - Fixed year (2024 → 2025)
      - Clarified prose vs structure distinction (OUTPUT vs INPUT)
      - Added 2025 sources
  - version: "0.1.0"
    date: 2025-12-19
    changes:
      - Initial research
---

# Research: LLM-Readable Markdown Design Patterns

## Executive Summary

Markdown's flat structure makes it ideal for LLM consumption—no nested tags, clear delimiters, natural tokenization. Key principles: **front-load critical information**, **avoid vague pronouns**, **use hierarchical headings**, **use structured formats (lists, tables)**, and **include structured metadata via YAML frontmatter**. Anthropic recommends XML tags for multi-component content boundaries.

## Research Goal

Understand optimal markdown structure for thinking LLMs. Inform creation of a `/md` command that produces documents with: YAML frontmatter (rationale, changelog, linked files), IDKW style, concise-yet-comprehensive content.

## Concept Overview

### Why Markdown for LLMs?

| Property | Benefit |
|----------|---------|
| Flat structure | No parsing overhead (unlike XML/JSON) |
| Clear delimiters | Unambiguous tokenization |
| Human-readable | What works for humans works for LLMs |
| Efficient | Fewer tokens than verbose formats |
| RAG-friendly | Natural chunking at heading boundaries |

### IDKW (Information Dense Keywords) Principles

1. **Front-load critical info** - Important content in headings and opening sentences
2. **Eliminate vague pronouns** - Restate subjects instead of "it", "this", "that"
3. **Structured lists over prose** - Better chunking, easier scanning
4. **Progressive disclosure** - General → specific, let reader drill down
5. **Unique headings** - Self-descriptive, aids retrieval
6. **Remove redundancy** - No boilerplate, no repetition

## How It Works

### Structural Hierarchy

```
# H1 - Document title (one per doc)
## H2 - Major sections
### H3 - Subsections
#### H4 - Details (use sparingly)
```

**Rules:**
- Never skip levels (H1 → H3 is wrong)
- Each heading = semantic boundary for chunking
- Headings should be unique and descriptive

### Content Blocks

| Block Type | Usage | LLM Benefit |
|------------|-------|-------------|
| Fenced code (```) | Code, configs, examples | Treated as single unit |
| Tables | Structured comparisons | Row/column scanning |
| Lists | Discrete items | Clear enumeration |
| Blockquotes | Quotes, callouts | Distinct voice/source |

### Anthropic's XML Tag Guidance

For multi-component content, XML tags outperform pure markdown:

```xml
<document>
  <source>file.md</source>
  <content>...</content>
</document>
```

**Recommended tags:**
- `<instructions>` - Behavioral directives
- `<example>` - Sample inputs/outputs
- `<document>` - Referenced content
- `<thinking>` - Reasoning traces
- `<answer>` - Final outputs

**When to use:** Multiple components, need clear boundaries, want parseable output.

### YAML Frontmatter Schema

```yaml
---
# Identity
title: "Document Title"
description: "One-sentence summary for retrieval"
version: "0.1.0"  # semver

# Provenance
author: "Name"
created: 2025-12-19
updated: 2025-12-19

# Classification
tags: ["keyword1", "keyword2"]
category: "type"

# Relationships
linked_files:
  - path/to/related.md
  - path/to/dependency.md

# Meta
rationale: |
  Why this document exists. What problem it solves.
  What decisions led to its current form.

changelog:
  - version: "0.1.0"
    date: 2025-12-19
    changes:
      - Initial creation
      - Added core sections
---
```

**Why each field matters:**

| Field | Purpose |
|-------|---------|
| `title` | Retrieval, identification |
| `description` | Search ranking, quick context |
| `version` | Track evolution, semver for compatibility |
| `rationale` | WHY decisions were made (critical for LLMs) |
| `changelog` | Evolution history, what changed when |
| `linked_files` | Dependency graph, related context |
| `tags` | Filtering, clustering |

## Best Practices

### Do

- **Use consistent terminology** - Same term for same concept throughout
- **Provide examples** - Code snippets, sample outputs (few-shot learning)
- **State constraints explicitly** - Prerequisites, valid ranges, scope
- **Include rationale** - WHY, not just WHAT (aids reasoning)
- **Keep paragraphs short** - 2-4 sentences max
- **Use tables for comparisons** - Options, trade-offs, matrices
- **Front-load each section** - Summary sentence first

### Don't

- **Over-format** - Excessive bold, italics, nested lists
- **Use vague references** - "it", "this", "that", "the above"
- **Skip heading levels** - H1 → H3 breaks hierarchy
- **Mix terminology** - "user" vs "customer" vs "client"
- **Nest deeply** - Lists within lists within lists
- **Include boilerplate** - Navigation, copyright, irrelevant metadata
- **Write wall-of-text** - Break into scannable chunks

### Anthropic-Specific (Clarification)

**Important distinction:**
- Claude 4.x "prefer prose" guidance = for Claude's **OUTPUT** (responses to users)
- For documents Claude **READS** (your use case) = structured formats win

**For LLM-readable INPUT documents:**
- **Use:** Lists, tables, headings, fenced code blocks
- **Why:** Better chunking, parsing, retrieval, scanning
- **Avoid:** Deep nesting, excessive formatting, vague pronouns

The "prose preference" prevents Claude from generating fragmented bullet-heavy responses. It does NOT apply to documents designed for LLM consumption.

## Integration Considerations

For the `/md` command:

1. **Template structure** - Enforce YAML frontmatter with required fields
2. **Validation** - Check heading hierarchy, flag vague pronouns
3. **Linked files** - Auto-populate from `@file` references in command
4. **Changelog** - Auto-initialize with 0.1.0 on creation
5. **IDKW enforcement** - Instruction to front-load, avoid pronouns

## Decision Points

Based on this research:

1. **Frontmatter schema**: Use rationale + changelog + linked_files (user requirement confirmed as best practice)
2. **Content style**: IDKW with structured formats (lists, tables for discrete/comparable items)
3. **Structure**: Hierarchical headings, tables for comparisons, code blocks for examples
4. **XML tags**: Optional for multi-component boundaries (separating documents, instructions, examples)

## Template Recommendation

```markdown
---
title: "$TITLE"
description: "$ONE_SENTENCE_SUMMARY"
version: "0.1.0"
created: $DATE
updated: $DATE
tags: [$TAGS]
linked_files: [$LINKED]
rationale: |
  $WHY_THIS_EXISTS
changelog:
  - version: "0.1.0"
    date: $DATE
    changes:
      - Initial creation
---

# $TITLE

## Summary

$FRONT_LOADED_OVERVIEW (2-3 sentences, key insight first)

## Context

$BACKGROUND_WHY_THIS_MATTERS

## [Main Sections]

$CONTENT_WITH_IDKW_STYLE

## References

$LINKED_SOURCES_IF_ANY
```

## Sources

| Source | Type | Date | Key Insight |
|--------|------|------|-------------|
| docs.claude.com (XML tags) | Official | 2025 | XML tags for multi-component boundaries |
| docs.claude.com (Claude 4 practices) | Official | 2025 | Prose pref = OUTPUT only, not INPUT docs |
| anthropics/courses | Official | 2025 | Structure: docs at top, instructions, XML, thinking space |
| mintlify.com/llm-readability | Article | 2025 | GEO principles, avoid pronouns, unique headings |
| developer.webex.com | Article | 2025 | Markdown outperforms JSON/XML for LLMs |
| bluehost.com/llms-txt | Article | 2025 | llms.txt standard, markdown structure mandatory |
| thenewstack.io/markdown-docs | Article | Dec 2025 | Best practices for app documentation |
| dev.to/llm-docs-optimization | Article | 2025 | Concise structured explanations, llms.txt adoption |
| github.com/frontmatter-format | Spec | 2025 | YAML frontmatter conventions for AI agents |
| docs.magi-mda.org | Spec | 2025 | Frontmatter for enhanced RAG performance |

## Queries Executed

| Query | Tool | Agent | Result |
|-------|------|-------|--------|
| "LLM-readable documentation best practices markdown structure" | Tavily | Concept | Hierarchy, chunking, flat structure benefits |
| "information dense keywords documentation technical writing" | Tavily | Concept | IDKW patterns, Six C's framework |
| Anthropic docs: structured prompts, XML tags | Context7 | Docs | XML tag recommendations, Claude 4 formatting |
| "prompt engineering structured output markdown" | Tavily | Ecosystem | Prompt-to-doc patterns |
| "YAML frontmatter AI documentation metadata" | Tavily | Ecosystem | Field standards, RAG optimization |
| "LLM-readable markdown documentation best practices 2025" | Tavily | Follow-up | Confirmed structured formats for INPUT docs |

## Open Questions

- **Optimal heading depth** - H4+ rarely needed, but unclear where to stop
- **Table vs list threshold** - When does a list become a table?
- **Changelog granularity** - Every edit or significant changes only?

## Follow-up Research

### Correction: Prose vs Structure (2025-12-19)

User flagged misapplication of Anthropic's "prefer prose" guidance. Clarification:
- Original finding conflated OUTPUT formatting with INPUT document design
- Anthropic's prose preference = how Claude should respond to users
- For LLM-readable documents (INPUT) = structured formats (lists, tables, headings) confirmed optimal
- 2025 sources (Mintlify, Webex, TheNewStack) all confirm structured markdown for LLM consumption

**Lesson:** Always distinguish between "content LLMs produce" vs "content LLMs consume".
