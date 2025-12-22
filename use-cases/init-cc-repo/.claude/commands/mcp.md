# MCP Tools Reference

## Behavior Directive

When user requests MCP tool usage:

1. **ASK before executing** - Do not assume parameters
2. **Present options** - Show relevant params from tables below
3. **Suggest defaults** - But confirm with user

Example interaction:
```
User: "search tavily for Claude Code best practices"
You: "Before searching, let me clarify:
- Depth: quick scan or thorough? (basic=1 credit, advanced=2 credits)
- Time: recent only? (week/month/year/all)
- Want direct answer? (include_answer)
- Max results: 5 (quick) or 15 (thorough)?
- Specific sites to include/exclude?"
```

---

## Context7

Fetch up-to-date library documentation.

### resolve-library-id

Find library ID first (required before get-library-docs).

| Param | Req | Description |
|-------|-----|-------------|
| `libraryName` | Yes | Library to find: "react", "nextjs", "fastapi" |

### get-library-docs

| Param | Req | Default | Options | When |
|-------|-----|---------|---------|------|
| `context7CompatibleLibraryID` | Yes | - | "/org/project" | From resolve-library-id |
| `topic` | No | - | "hooks", "routing", "auth" | Focus area |
| `mode` | No | "code" | `code`, `info` | code=API+examples, info=concepts+guides |
| `page` | No | 1 | 1-10 | Paginate for more context |

**Workflow**:
1. `resolve-library-id` → get ID
2. `get-library-docs` with ID + topic

---

## Tavily

### Credit Costs

| Operation | Cost |
|-----------|------|
| Basic search | 1 credit |
| Advanced search | 2 credits |
| Basic extract (5 URLs) | 1 credit |
| Advanced extract (5 URLs) | 2 credits |

### tavily-search

| Param | Req | Default | Options | When |
|-------|-----|---------|---------|------|
| `query` | Yes | - | string | The search |
| `search_depth` | No | "basic" | `basic`, `advanced` | advanced = AI post-processing, LLM-optimized |
| `topic` | No | "general" | `general`, `news`, `finance` | Category filter |
| `max_results` | No | 10 | 5-20 | 5=quick, 15=thorough |
| `time_range` | No | all | `day`, `week`, `month`, `year` | Recency filter |
| `days` | No | 3 | number | News topic only |
| `include_answer` | No | false | `true`, `"basic"`, `"advanced"` | LLM-generated answer from results |
| `chunks_per_source` | No | 3 | 1-3 | Content snippets per source (advanced only) |
| `include_domains` | No | [] | ["docs.anthropic.com"] | Whitelist sites |
| `exclude_domains` | No | [] | ["reddit.com"] | Blacklist sites |
| `include_raw_content` | No | false | `true`, `"markdown"`, `"text"` | Full parsed content |
| `include_images` | No | false | boolean | Image results |
| `include_image_descriptions` | No | false | boolean | AI descriptions of images |

**Quick patterns**:
- Quick lookup: `search_depth: basic, max_results: 5`
- Deep research: `search_depth: advanced, max_results: 15`
- Q&A with answer: `include_answer: "advanced"`
- Recent news: `topic: news, time_range: week`
- Official docs: `include_domains: ["docs.X.com"]`
- Concise results: `chunks_per_source: 1`

### tavily-extract

| Param | Req | Default | Options | When |
|-------|-----|---------|---------|------|
| `urls` | Yes | - | ["url1", "url2"] | Known URLs to extract |
| `extract_depth` | No | "basic" | `basic`, `advanced` | advanced = LinkedIn, complex pages |
| `format` | No | "markdown" | `markdown`, `text` | Output format |
| `include_images` | No | false | boolean | Extract images |
| `include_favicon` | No | false | boolean | Favicon URLs |

**When to use**:
- `search` → Find relevant pages
- `extract` → Get full content from known URLs

---

## Ask Checklist

For **tavily-search**, always clarify:
- [ ] Depth? (basic=1cr / advanced=2cr)
- [ ] Time filter? (day/week/month/year/all)
- [ ] Want direct answer? (include_answer)
- [ ] Result count? (5/10/15)
- [ ] Site restrictions? (include/exclude domains)

For **tavily-extract**, always clarify:
- [ ] Which URLs?
- [ ] Depth? (basic/advanced)
- [ ] Format? (markdown/text)

For **context7**, always clarify:
- [ ] Which library exactly?
- [ ] Specific topic/feature?
- [ ] Code examples or conceptual info?

---

## Best Practices

1. **Context efficiency** - Only use MCP tools when needed
2. **`include_answer: true`** - Great for Q&A, provides synthesized answer
3. **`chunks_per_source: 1`** - Reduce for concise results
4. **Advanced search** - Worth 2x cost for LLM-optimized content
5. **Domain filtering** - Use `include_domains` for authoritative sources
