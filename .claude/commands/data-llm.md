# Data LLM Context

**Phase 5 of 5** in the data analyst workflow.

## Purpose

Generate a comprehensive context document that enables an LLM/SQL agent to understand and query this data correctly. This phase answers: What does an AI need to know to write accurate SQL?

## Workflow

1. **Read philosophy first**
   - Read `.claude/skills/data-analyst/cookbook/philosophy.md`
   - Remember: "Schema is necessary but insufficient. LLMs need semantic context."

2. **Read the WHY**
   - Read `.claude/skills/data-analyst/cookbook/llm/why.md`
   - Explain WHY LLM context is SEPARATE from validation

3. **Gather all prior phase outputs**
   - Read `ai-docs/data-understand-{project}.md` → business context
   - Read `ai-docs/data-explore-{project}.md` → data shape, issues
   - Read `ai-docs/data-clean-{project}.md` → transformations applied
   - Read `ai-docs/data-validate-{project}.md` → quality metrics
   - If any phase missing, note the gap

4. **Extract schema information**
   - Identify all clean data tables
   - For each table:
     - Row count
     - Grain (one row = one what?)
     - Columns with types
     - Primary/foreign keys
     - NULL rates
     - Categorical values (enums)
     - Temporal boundaries

5. **Document relationships**
   - Map foreign key relationships
   - Note cardinality (1:1, 1:N, N:M)
   - Note coverage rates (e.g., "64% of SMS have shop_id")

6. **Compile data limits**
   - Read `cookbook/llm/limits.md` for patterns
   - Document:
     - Coverage gaps (unlinked records)
     - Missing dimensions (no revenue, no demographics)
     - Temporal boundaries
   - Write agent response templates for each limit

7. **Build domain glossary**
   - Read `cookbook/llm/glossary.md` for patterns
   - Map business terms to SQL:
     - Metrics (NPS, rating, etc.)
     - Entities (shop, customer, etc.)
     - Categories (enum values)
     - Synonyms (unhappy → detractor)

8. **Create query patterns**
   - Read `cookbook/llm/queries.md` for templates
   - Document proven patterns for this data:
     - Aggregation by dimension
     - Top/bottom N
     - Time series
     - Segment comparison
   - Document ANTI-PATTERNS (what NOT to do)

9. **Produce context document**
   - Write to `ai-docs/data-llm-{project-slug}.md`
   - Follow this structure:
     - TL;DR (what tables, what questions can be answered)
     - Schema Overview (with semantic annotations)
     - Relationships (text-based ERD)
     - Data Limits (CAN/CANNOT lists)
     - Query Patterns (proven recipes)
     - Anti-Patterns (what to avoid)
     - Domain Glossary (term → SQL)
     - Temporal Boundaries

## Output Structure

```markdown
---
phase: llm
project: {project-name}
date: {ISO timestamp}
source_phases:
  - data-understand: {filename}
  - data-explore: {filename}
  - data-clean: {filename}
  - data-validate: {filename}
---

# Data Context: {Project Name}

## TL;DR
[One paragraph: what data, what questions it can answer, key limits]

## Schema Overview
### {table_name} ({row_count} rows) — {grain}
| Column | Type | Meaning | Example | Notes |
...

## Relationships
```
{text-based ERD}
```

## Data Limits
> These limits affect what questions can be answered.

### What You CAN Answer
- ...

### What You CANNOT Answer
- ...

### Coverage Gaps
| Limitation | Records | Impact | Agent Response |
...

## Query Patterns
### Pattern 1: {Name}
```sql
...
```

### Anti-Pattern: {What NOT to do}
```sql
-- WRONG: ...
-- RIGHT: ...
```

## Domain Glossary
| Term | Definition | SQL |
...

## Temporal Boundaries
| Table | Column | Start | End |
...
```

## Code Execution

When generating context:
- Use Python to extract schema from clean data files
- Follow patterns from `cookbook/llm/code.md`
- Read actual data to get accurate counts, ranges, enums
- Merge technical schema with semantic meanings from prior phases

## Rules

- **SINGLE DOCUMENT** - All context in one file (for injection)
- **EXPLICIT over IMPLIED** - State everything, assume nothing
- **LIMITS are FIRST-CLASS** - Don't bury gaps in footnotes
- **GLOSSARY maps to SQL** - Every term needs a SQL equivalent
- **ANTI-PATTERNS are REQUIRED** - Prevent common mistakes

## Argument

If user provides `$ARGUMENTS`:
- Treat as project name or slug
- Example: `/data-llm orange-cx-intelligence`
- Will look for `ai-docs/data-*-orange-cx-intelligence.md` files

## Success Criteria

The document is complete when an LLM can:

| Capability | Test |
|------------|------|
| Understand schema | List all tables and their grain |
| Know limits | State what questions CANNOT be answered |
| Write correct SQL | Join tables without data loss |
| Use business terms | Map "unhappy customer" to SQL |
| Caveat appropriately | Mention coverage gaps in responses |

## Integration

This document is designed for **context injection**:

```
System: You are a SQL agent. Here is your data context:
{contents of data-llm-{project}.md}

User: Show me which regions have declining NPS.
Agent: [reads context, generates correct SQL, states caveats]
```
