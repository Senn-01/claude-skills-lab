---
topic: "Information Dense Keywords (IDK) for Reasoning LLMs"
date: 2025-12-19T15:30:00Z
status: complete
tools_used: [tavily, context7]
queries_executed: 8
agents_spawned: 4
version: 1.0.0
---

# Information Dense Keywords (IDK)

> A curated reference of high-signal prompting vocabulary for reasoning LLMs.

## Executive Summary

"Information Dense Keywords" (IDK) refers to **high-signal words and phrases that trigger specific LLM behaviors with minimal tokens**. While not a formally established term, the concept represents the evolution from verbose prompting to precision vocabulary that activates reasoning, controls output, and shapes model behavior efficiently.

**Critical 2025 Insight**: Reasoning models (Claude 3.7+, o1, DeepSeek R1, Gemini 2.5 Pro) have native reasoning capabilities. Traditional CoT prompts like "think step by step" are now often **counterproductive**—they create redundancy with built-in reasoning. The paradigm has shifted to **Chain-of-Draft**: concise intermediate thoughts that capture only essential information.

---

## The IDK Framework

### What Makes a Keyword "Dense"?

| Property | Description |
|----------|-------------|
| **Signal-to-Token Ratio** | Maximum behavioral change per token spent |
| **Trigger Specificity** | Activates a precise, predictable behavior |
| **Model Alignment** | Maps to how LLMs were trained (RLHF patterns) |
| **Composability** | Stacks well with other keywords |

### Density Spectrum

```
LOW DENSITY                                    HIGH DENSITY
"help me"  →  "explain"  →  "analyze"  →  "act as [role]"  →  XML tags
```

---

## IDK Taxonomy

### 1. Reasoning Triggers

Keywords that activate analytical processing and logical decomposition.

| Keyword/Phrase | Effect | Use With |
|----------------|--------|----------|
| `Let's think step by step` | Activates CoT reasoning | Non-reasoning models |
| `Show your work` | Exposes reasoning process | Math, logic tasks |
| `Break down` | Triggers decomposition | Complex problems |
| `Analyze` | Deep examination mode | Any analytical task |
| `Walk through` | Sequential processing | Processes, workflows |
| `First... then...` | Forces sequential execution | Multi-step tasks |

**2025 Note**: For reasoning models (Claude 3.7+, o1), omit explicit CoT triggers. They reason natively.

### 2. Output Structure

Keywords controlling format and organization.

| Keyword | Effect | Example Usage |
|---------|--------|---------------|
| `Concise` | Brief, focused output | "Provide a concise summary" |
| `Bullet-pointed` | List format | "Give me bullet-pointed key insights" |
| `JSON format` | Structured data output | "Return results in JSON format" |
| `Table` | Tabular presentation | "Present as a comparison table" |
| `In [N] sentences` | Length constraint | "Summarize in three sentences" |
| `Outline` | Hierarchical structure | "Create an outline of the argument" |

**Power Stack**: `"Provide a concise, bullet-pointed summary in 5 items"`

### 3. Role/Persona

Keywords establishing identity and expertise domain.

| Keyword | Effect | When to Use |
|---------|--------|-------------|
| `Act as [role]` | Primary persona trigger | Domain-specific tasks |
| `You are [expert]` | Identity establishment | Consistent expertise |
| `As a [specialist]` | Domain framing | Technical accuracy |
| `Respond as` | Behavioral framing | Tone/style control |

**Effective Roles**:
- `senior data analyst` - analytical rigor
- `cybersecurity expert` - security focus
- `teacher` - explanatory mode
- `consultant` - advisory perspective

**2025 Best Practice**: Combine role with specific constraints:
```
You are a senior backend engineer. Focus only on performance implications.
```

### 4. Quality Controls

Keywords ensuring accuracy and appropriate tone.

| Keyword | Effect |
|---------|--------|
| `Accurate` | Precision requirement |
| `Verified` | Request validation |
| `Actionable` | Practical application focus |
| `Professional` | Business-appropriate tone |
| `Empathetic` | Compassionate response |
| `Data-driven` | Evidence-based output |

**Anti-Hallucination Pattern**:
```
If you don't know, say "I don't know." Quote relevant sources first.
```

### 5. Constraints & Boundaries

Keywords defining scope and requirements.

| Keyword | Effect | Example |
|---------|--------|---------|
| `Only` | Hard limitation | "Only include items from 2025" |
| `Never` | Prohibition | "Never mention competitor names" |
| `Must` | Mandatory requirement | "Must include error handling" |
| `Avoid` | Soft exclusion | "Avoid technical jargon" |
| `Exactly [N]` | Precise quantity | "Exactly 5 bullet points" |
| `Focus on` | Priority direction | "Focus on security implications" |

### 6. XML Tags (Highest Density)

Structural keywords that separate prompt components unambiguously.

| Tag | Purpose |
|-----|---------|
| `<instructions>` | Core task definition |
| `<context>` | Background information |
| `<example>` | Sample input/output pairs |
| `<thinking>` | Reasoning container (for structured CoT) |
| `<answer>` | Final output container |
| `<document>` | Reference material wrapper |

**Pattern**:
```xml
<instructions>
Analyze the code for security vulnerabilities.
</instructions>

<context>
This is a payment processing module.
</context>

<output_format>
Return findings as a numbered list with severity ratings.
</output_format>
```

---

## 2025 Paradigm Shifts

### Chain-of-Draft Replaces Chain-of-Thought

| Old (CoT) | New (CoD) |
|-----------|-----------|
| "Let's think step by step..." | Let the model reason natively |
| Verbose intermediate steps | Concise essential-only drafts |
| Explicit reasoning prompts | Problem structure clarity |
| Token-heavy | Token-efficient |

**Research Insight**: Humans naturally draft concise intermediate thoughts. Chain-of-Draft mirrors this, producing faster, more efficient reasoning.

### Reasoning Models Don't Need CoT Prompts

| Model | Native Reasoning | CoT Prompt Effect |
|-------|------------------|-------------------|
| Claude 3.7+ | Yes (extended thinking) | Counterproductive |
| OpenAI o1/o3 | Yes (multi-step logic) | Redundant |
| DeepSeek R1 | Yes (self-verification) | Unnecessary |
| Gemini 2.5 Pro | Yes (adjustable effort) | Usually redundant |

**Best Practice Flow**:
1. Try without reasoning prompts first
2. If shallow results → enable low thinking effort
3. Increase effort only if needed (low → medium → high)
4. Optimize for accuracy, then latency/cost

### Context Engineering > Prompt Engineering

The term "context engineering" reflects that every instruction is a product decision. Modern approach:

1. **Structure** context with XML tags
2. **Place** long documents at top, queries at bottom
3. **Ground** with examples (3-5 diverse, relevant)
4. **Constrain** explicitly what to include/exclude
5. **Prefill** responses to skip preambles

---

## Claude-Specific IDKs

### Anthropic Official Recommendations

| Technique | Keywords/Pattern |
|-----------|------------------|
| **Structured CoT** | Use `<thinking>` and `<answer>` tags |
| **Prefilling** | Start response with `{` for JSON, `[ROLE]` for persona |
| **Long Context** | "Quote relevant parts first" + documents at top |
| **Anti-Hallucination** | "If you don't know, say 'I don't know'" |

### Claude 4.x Specific

Claude 4 models (Sonnet 4.5, Haiku 4.5) are trained for **precise instruction following**. They won't infer extras.

**Required Modifiers for Claude 4**:
- `"Include as many relevant features and interactions as possible"`
- `"Go beyond the basics to create a fully-featured implementation"`
- Be explicit—these models follow instructions literally

### Extended Thinking Keywords

For Claude's extended thinking mode:

| Prompt Type | Effect |
|-------------|--------|
| `"Think deeply about this problem"` | General reasoning activation |
| `<thinking_example>` tags | Show HOW to think through problems |
| Increase budget + request longer output | For 20K+ word generation |

**Do NOT**:
- Pass thinking blocks back in conversation
- Use prefilling with extended thinking
- Use explicit CoT prompts (redundant)

---

## IDK Stacking Patterns

### Maximum Density Stack

```
Act as a senior security engineer.
Analyze this code for OWASP Top 10 vulnerabilities.
Provide a concise, bullet-pointed report.
Focus only on critical and high severity issues.
If you find none, say "No critical vulnerabilities found."
```

**Density Analysis**:
- Role: `senior security engineer`
- Task: `Analyze` + specific domain
- Format: `concise, bullet-pointed`
- Constraint: `only critical and high`
- Anti-hallucination: explicit fallback

### RTFD Framework

| Component | IDKs Used |
|-----------|-----------|
| **R**ole | `Act as`, `You are`, `As a` |
| **T**ask | `Analyze`, `Create`, `Review`, `Explain` |
| **F**ormat | `Bullet-pointed`, `JSON`, `Table`, `In [N] sentences` |
| **D**etails | `Focus on`, `Only`, `Must include`, `Avoid` |

---

## Anti-Patterns (What NOT to Do)

| Anti-Pattern | Why It Fails | Fix |
|--------------|--------------|-----|
| "Make this better" | Too vague | Specify dimensions: "Make this more concise and professional" |
| CoT prompts with reasoning models | Redundant, wastes tokens | Omit; let native reasoning work |
| Instructions after long context | Buried, forgotten | Documents TOP, queries BOTTOM |
| "Give me exactly 500 words" | LLMs count tokens, not words | Use sentence/paragraph counts |
| Implicit expectations | Claude lacks your context | Be explicit about everything |
| Missing examples for complex tasks | Model guesses format | Provide 3-5 diverse examples |

---

## Quick Reference Card

### Top 10 Most Dense Keywords

1. **`Act as [role]`** - Instant domain expertise
2. **`<xml_tags>`** - Unambiguous structure
3. **`Concise`** - Brevity signal
4. **`Analyze`** - Deep processing mode
5. **`Only`** - Hard constraint
6. **`If you don't know, say so`** - Anti-hallucination
7. **`First... then...`** - Sequential execution
8. **`JSON format`** - Structured output
9. **`Focus on`** - Attention direction
10. **`Quote relevant parts`** - Grounding (long context)

### Model-Appropriate Triggers

| Model Type | Use | Avoid |
|------------|-----|-------|
| **Reasoning (Claude 3.7+, o1)** | Clear problem structure, constraints | "Think step by step" |
| **Standard (GPT-4, Claude 3)** | CoT triggers, explicit reasoning | Assuming native reasoning |
| **Fast (Haiku, GPT-4-mini)** | Simple keywords, clear format | Complex chains |

---

## Sources

### Primary Research

| Source | Contribution |
|--------|--------------|
| [Anthropic Prompt Engineering Docs](https://platform.claude.com/docs) | Official Claude techniques |
| [Prompting Guide - Reasoning LLMs](https://www.promptingguide.ai/guides/reasoning-llms) | 2025 reasoning model practices |
| [Chain of Draft Paper (arXiv)](https://arxiv.org/pdf/2502.18600) | CoD vs CoT research |
| [Getzep - Reasoning Models](https://www.getzep.com/ai-agents/prompt-engineering-for-reasoning-models/) | o1/Claude 3.7 specific techniques |

### Community Wisdom

| Source | Insight |
|--------|---------|
| [Aakash Gupta - Prompt Engineering 2025](https://www.news.aakashg.com/p/prompt-engineering) | Context engineering as product strategy |
| [Reddit r/PromptEngineering](https://www.reddit.com/r/PromptEngineering/) | Advanced techniques, effectiveness metrics |
| [Sebastian Raschka - Reasoning Inference](https://magazine.sebastianraschka.com/p/state-of-llm-reasoning-and-inference-scaling) | Wait tokens, inference scaling |

### Reference Collections

| Source | Type |
|--------|------|
| [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) | Replicable code samples |
| [Prompt Engineering Examples](https://www.newline.co/@Dipen/top-10-prompt-engineering-examples-for-refining-llms-with-newline--f6945ac5) | Practical patterns |
| [Analytics Vidhya - 17 Techniques](https://www.analyticsvidhya.com/blog/2024/10/17-prompting-techniques-to-supercharge-your-llms/) | Comprehensive taxonomy |

---

## Open Questions

1. **How will IDKs evolve with multimodal models?** Vision + text may require new keywords.
2. **Will extended thinking become default?** Anthropic hints reasoning will standardize.
3. **Cross-model portability?** Some IDKs work universally; others are model-specific.

---

## Follow-up Research

*[Section reserved for future queries on this topic]*
