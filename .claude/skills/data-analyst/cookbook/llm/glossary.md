# Domain Glossary Patterns

## The Goal

Create a translation layer between:
- **Business language** (what users say)
- **Data language** (what columns/values exist)
- **SQL language** (how to query it)

---

## Why Glossaries Matter

### Without Glossary

User: "Show me unhappy customers"
Agent: "I don't have a column called 'unhappy'. Could you clarify?"

### With Glossary

User: "Show me unhappy customers"
Agent: (looks up "unhappy" → detractor → `nps_score <= 6`)
Agent: Generates correct SQL

---

## Glossary Structure

### Basic Format

```markdown
## Domain Glossary

| Term | Definition | SQL Mapping |
|------|------------|-------------|
| NPS | Net Promoter Score (0-10) | `nps_score` column |
| Promoter | Customer scoring 9-10 | `WHERE nps_score >= 9` |
| Detractor | Customer scoring 0-6 | `WHERE nps_score <= 6` |
| Passive | Customer scoring 7-8 | `WHERE nps_score IN (7, 8)` |
```

### Extended Format (Recommended)

```markdown
## Domain Glossary

### Customer Feedback Terms

| Term | Also Called | Definition | SQL Mapping | Notes |
|------|-------------|------------|-------------|-------|
| NPS | Net Promoter Score | Loyalty metric 0-10 | `nps_score` | Higher = better |
| Promoter | Happy customer, advocate | NPS 9-10 | `nps_score >= 9` | Likely to recommend |
| Detractor | Unhappy customer | NPS 0-6 | `nps_score <= 6` | Risk of churn |
| Passive | Neutral | NPS 7-8 | `nps_score BETWEEN 7 AND 8` | Satisfied but not loyal |
| Verbatim | Comment, feedback text | Free-text response | `verbatim` column | 78% NULL |
```

---

## Synonym Handling

Users don't always use exact terms. Map synonyms:

```markdown
### Synonym Mappings

| User Might Say | Maps To | SQL |
|----------------|---------|-----|
| "unhappy", "dissatisfied", "angry" | Detractor | `nps_score <= 6` |
| "happy", "satisfied", "loyal" | Promoter | `nps_score >= 9` |
| "good shops", "top performers" | High-rated | `AVG(rating) >= 4` |
| "bad shops", "problem shops" | Low-rated | `AVG(rating) < 3` |
| "feedback", "reviews", "comments" | Verbatim text | `verbatim` column |
| "recently", "latest" | Recent period | `date >= DATE_SUB(MAX(date), INTERVAL 30 DAY)` |
```

---

## Entity Glossary

Define what business entities mean:

```markdown
### Business Entities

| Entity | Definition | Table | Key Column |
|--------|------------|-------|------------|
| Shop | Retail location (physical store) | `dim_shops` | `shop_id` |
| MOBIS | Internal shop identifier code | `dim_shops` | `mobis_code` |
| Franchise | Partner-owned shop | `dim_shops` | `macro_segment = 'FRANCHISE'` |
| Own | Company-owned shop | `dim_shops` | `macro_segment = 'OWN'` |
| Corner | Small kiosk format | `dim_shops` | `macro_segment = 'CORNER'` |
| Region | Geographic area | `dim_shops` | `region` column |
```

---

## Metric Glossary

Define business metrics and their calculations:

```markdown
### Business Metrics

| Metric | Definition | Calculation | Table |
|--------|------------|-------------|-------|
| NPS Score | Net Promoter Score | `% promoters - % detractors` | `fact_sms_surveys` |
| Average Rating | Mean star rating | `AVG(rating)` | `fact_google_reviews` |
| Review Volume | Count of reviews | `COUNT(*)` | `fact_google_reviews` |
| Response Rate | % surveys completed | `completed / sent * 100` | N/A (not in data) |
```

### Derived Metrics (Agent Can Calculate)

```markdown
| Metric | User Asks | SQL Calculation |
|--------|-----------|-----------------|
| NPS | "What's the NPS?" | `100 * (COUNT(CASE WHEN nps >= 9) - COUNT(CASE WHEN nps <= 6)) / COUNT(*)` |
| % Detractors | "How many unhappy customers?" | `100.0 * COUNT(CASE WHEN nps <= 6 THEN 1 END) / COUNT(*)` |
| Trend | "Is it improving?" | Compare current period AVG to previous period AVG |
```

---

## Categorical Value Glossary

Map business concepts to actual enum values:

```markdown
### Categorical Values

#### Shop Types (`macro_segment` column)

| Business Term | Column Value | Meaning |
|---------------|--------------|---------|
| Franchise shop | `FRANCHISE` | Partner-owned, licensed operation |
| Company shop | `OWN` | Directly owned by company |
| Kiosk | `CORNER` | Small format, often in malls |
| Closed | `CLOSED` | Defunct, exclude from analysis |

#### Languages (`language` column)

| Business Term | Column Value | Meaning |
|---------------|--------------|---------|
| French-speaking | `FR` | Wallonia region |
| Dutch-speaking | `NL` | Flanders region |
| Bilingual | `BI` | Brussels region |

#### Rating Levels (`rating` column)

| Business Term | Value Range | Meaning |
|---------------|-------------|---------|
| Excellent | 5 | Best rating |
| Good | 4 | Above average |
| Average | 3 | Neutral |
| Poor | 2 | Below average |
| Terrible | 1 | Worst rating |
```

---

## Time Period Glossary

Help agent interpret temporal language:

```markdown
### Time Periods

| User Says | Interpretation | SQL |
|-----------|----------------|-----|
| "this month" | Current calendar month | `DATE_TRUNC('month', CURRENT_DATE)` |
| "last month" | Previous calendar month | `DATE_TRUNC('month', DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH))` |
| "this quarter" | Current Q | `DATE_TRUNC('quarter', CURRENT_DATE)` |
| "YTD" | Year to date | `date >= DATE_TRUNC('year', CURRENT_DATE)` |
| "recent", "lately" | Last 30 days | `date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)` |
| "historically" | All available data | No date filter |

**Note**: Data range is 2023-01-01 to 2024-06-30. Queries outside this range return no results.
```

---

## Aggregation Glossary

Map summary language to SQL:

```markdown
### Aggregation Terms

| User Says | SQL Function | Notes |
|-----------|--------------|-------|
| "average", "mean" | `AVG()` | |
| "total", "sum" | `SUM()` | |
| "count", "how many" | `COUNT(*)` | |
| "unique", "distinct" | `COUNT(DISTINCT)` | |
| "highest", "maximum" | `MAX()` | |
| "lowest", "minimum" | `MIN()` | |
| "typical", "median" | `PERCENTILE_CONT(0.5)` | Not all DBs support |
| "spread", "variation" | `STDDEV()` | |
```

---

## Comparison Language

```markdown
### Comparison Terms

| User Says | Interpretation | Example SQL |
|-----------|----------------|-------------|
| "more than", "above", "over" | `>` | `rating > 3` |
| "less than", "below", "under" | `<` | `nps < 7` |
| "at least", "minimum" | `>=` | `COUNT(*) >= 5` |
| "at most", "maximum" | `<=` | `rating <= 2` |
| "between X and Y" | `BETWEEN` | `nps BETWEEN 7 AND 8` |
| "top N", "best N" | `ORDER BY DESC LIMIT N` | |
| "bottom N", "worst N" | `ORDER BY ASC LIMIT N` | |
```

---

## Building the Glossary

### Sources

1. **Business Understanding doc**: Stakeholder terminology
2. **Data Exploration doc**: Actual column values found
3. **Data Cleaning doc**: Transformations that renamed/mapped values
4. **Domain expertise**: Industry-standard terms (NPS, CSAT, etc.)

### Process

1. Extract all unique categorical values from data
2. Map business terms to column names
3. Document synonyms users might use
4. Define derived metrics with formulas
5. Include "Also Called" alternatives

---

## Output Format

In final LLM context document:

```markdown
## Domain Glossary

### Core Metrics

| Term | Definition | SQL |
|------|------------|-----|
| NPS | Net Promoter Score (0-10) | `nps_score` |
| Promoter | Loyal customer (NPS 9-10) | `WHERE nps_score >= 9` |
| Detractor | At-risk customer (NPS 0-6) | `WHERE nps_score <= 6` |
| Rating | Google review stars (1-5) | `rating` |

### Entity Types

| Term | Definition | SQL |
|------|------------|-----|
| Shop | Retail location | `dim_shops` table |
| Franchise | Partner-owned shop | `macro_segment = 'FRANCHISE'` |
| Own | Company-owned shop | `macro_segment = 'OWN'` |

### Synonyms (User → System)

| User Says | Means | SQL |
|-----------|-------|-----|
| "unhappy customer" | Detractor | `nps_score <= 6` |
| "problem shop" | Low-rated | `AVG(rating) < 3` |
| "French region" | Wallonia | `language = 'FR'` |
```

---

## Glossary Checklist

- [ ] All columns have business definitions
- [ ] All categorical values mapped to business terms
- [ ] Common synonyms documented
- [ ] Derived metrics have formulas
- [ ] Time period language mapped
- [ ] Aggregation terms defined
- [ ] Comparison language documented
- [ ] Industry terms explained (NPS, CSAT, etc.)
