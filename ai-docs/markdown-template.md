---
description: Generate LLM-readable markdown with YAML frontmatter, IDKW style
argument-hint: [topic or filename]
---

# Markdown Generator

Generate a markdown file optimized for LLM consumption.

**Topic/File**: $ARGUMENTS

---

## Your Preferences (MANDATORY)

### YAML Frontmatter (REQUIRED)

Every markdown file MUST start with this frontmatter structure:

```yaml
---
title: "Descriptive Title"
description: "One-sentence summary for retrieval"
version: "0.1.0"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [keyword1, keyword2]
linked_files:
  - path/to/related.md
rationale: |
  WHY this document exists. What problem it solves.
  What decisions led to its current form.
changelog:
  - version: "0.1.0"
    date: YYYY-MM-DD
    changes:
      - Initial creation
---
```

**Required fields**: title, version, rationale, changelog
**Semver**: Always start at 0.1.0

---

## IDKW Writing Style (Information Dense Keywords)

| Principle | Implementation |
|-----------|----------------|
| **Front-load** | Put critical info in headings and first sentences |
| **No vague pronouns** | Restate subjects. Never use "it", "this", "that" without antecedent |
| **Structured formats** | Lists for discrete items, tables for comparisons |
| **Progressive disclosure** | General → specific, drill-down structure |
| **Unique headings** | Each heading self-descriptive, aids retrieval |
| **No redundancy** | Remove boilerplate, repetition |

---

## Structural Rules

### Heading Hierarchy
- One H1 (title) per document
- Never skip levels (H1 → H3 is WRONG)
- H2 for major sections
- H3 for subsections
- H4 sparingly for details

### Content Blocks

| Block | When to Use |
|-------|-------------|
| **Lists** | Discrete items, steps, enumerations |
| **Tables** | Comparisons, options, matrices, key-value pairs |
| **Code blocks** | Code, configs, examples (always with language identifier) |
| **Blockquotes** | Quotes, callouts, important notes |

### Anti-Patterns (AVOID)

- Wall of text without structure
- Skipping heading levels
- Vague pronouns without clear antecedent
- Deep nesting (lists within lists within lists)
- Excessive bold/italics
- Missing rationale (WHY not just WHAT)

---

## Output Format

```markdown
---
title: "[Generated Title]"
description: "[One sentence]"
version: "0.1.0"
created: [today's date]
updated: [today's date]
tags: [relevant, keywords]
linked_files: []
rationale: |
  [WHY this doc exists]
changelog:
  - version: "0.1.0"
    date: [today's date]
    changes:
      - Initial creation
---

# [Title]

## Summary

[2-3 sentences, key insight first, front-loaded]

## [Main Sections with Logical Structure]

[Content following IDKW principles]

## References

[Sources if applicable]
```

---

## Behavior

1. If `$ARGUMENTS` is empty → ASK user what document to create
2. If `$ARGUMENTS` is a filename → Create that file
3. If `$ARGUMENTS` is a topic → Propose filename, confirm, then create
4. ALWAYS use today's actual date
5. ALWAYS include rationale explaining WHY the document exists
6. ALWAYS use structured formats (lists, tables) over prose paragraphs
