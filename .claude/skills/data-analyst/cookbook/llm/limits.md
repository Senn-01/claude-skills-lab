# Documenting Data Limits

## The Principle

> "An honest agent states what it cannot do as clearly as what it can."

Data limits are not footnotes. They are first-class information that determines whether the agent can answer a question correctly—or at all.

---

## Why Limits Matter for LLMs

### Without Limits Documentation

User: "What's the average NPS by shop?"
Agent: Returns result using INNER JOIN, silently dropping 36% of data.
User: Makes decision based on incomplete data.

### With Limits Documentation

User: "What's the average NPS by shop?"
Agent: Returns result with caveat: "Note: This covers 64% of SMS surveys. 36% cannot be linked to shops and are excluded from this analysis."
User: Understands the scope and can ask follow-up questions.

---

## Types of Limits

### 1. Coverage Limits

Data exists but is incomplete or partial.

```markdown
| Limitation | Scope | Impact |
|------------|-------|--------|
| 36% SMS unlinked | 1,897 of 5,268 records | Cannot group by shop |
| 28 unknown MOBIS | 1,218 SMS records | Orphan records |
| 78% empty verbatims | 1,416 of 1,815 reviews | Limited text analysis |
```

### 2. Temporal Limits

Data only covers certain time periods.

```markdown
| Table | Date Range | Gap |
|-------|------------|-----|
| fact_google_reviews | 2023-01 to 2024-06 | No 2022 data |
| fact_sms_surveys | 2024-01 to 2024-06 | No 2023 data |
```

### 3. Scope Limits

Data doesn't include certain entities or dimensions.

```markdown
| What's Missing | Impact |
|----------------|--------|
| No revenue data | Cannot tie CX to financial outcomes |
| No customer demographics | Cannot segment by age/gender |
| No competitor data | Cannot benchmark externally |
```

### 4. Quality Limits

Data exists but has known issues.

```markdown
| Issue | Scope | Handling |
|-------|-------|----------|
| 24 duplicate review_ids | 24 records | Flagged, not removed |
| 3 NULL ratings | 3 reviews | Excluded from avg calculations |
```

---

## Limit Documentation Template

### Section Format

```markdown
## Data Limits

> These limits affect what questions can be answered. The agent MUST mention relevant limits when answering questions.

### Coverage Limits

| Limitation | Affected Records | Impact | Agent Response |
|------------|------------------|--------|----------------|
| 36% SMS have NULL shop_id | 1,897 of 5,268 | Cannot join to dim_shops | "This covers 64% of SMS data (those linked to shops)" |
| 28 MOBIS codes not in master | 1,218 SMS | Cannot enrich with shop details | "Some surveys reference shops not in our master data" |
| 78% verbatims empty | 1,416 of 1,815 reviews | Limited text analysis | "Most reviews don't have text comments" |

### Questions You CANNOT Answer

| Question Type | Why Not | Alternative |
|---------------|---------|-------------|
| "Revenue impact of low NPS" | No revenue data | "Can show NPS trends, but not financial correlation" |
| "Customer demographics by shop" | No demographics | "Can show feedback volume and scores only" |
| "Compare to competitors" | No competitor data | "Can only show internal trends" |
| "Full SMS analysis by shop" | 36% unlinked | "Can analyze by MOBIS code instead, or caveat shop analysis" |

### Questions You CAN Answer (with caveats)

| Question | Caveat Required |
|----------|-----------------|
| "NPS by shop" | "Covers 64% of SMS data" |
| "Rating trends over time" | "Google reviews only, starts 2023-01" |
| "Top/bottom shops by feedback" | "Based on linked surveys only" |
```

---

## Writing Agent Response Templates

For each major limit, provide the exact language the agent should use:

### Pattern

```markdown
**Limit**: 36% of SMS surveys have NULL shop_id

**When triggered**: Any query grouping SMS data by shop attributes

**Agent must say**:
"Note: This analysis covers 64% of SMS surveys (3,371 of 5,268 records).
The remaining 36% cannot be linked to shops in our master data and are
excluded. These unlinked surveys can be analyzed by MOBIS code or channel
instead."
```

### Examples

```markdown
### Limit: Incomplete Shop Master

**Trigger**: Joining fact tables to dim_shops
**Agent response**: "This analysis uses {N} of {total} records ({pct}%).
{excluded} records reference shops not in our master data."

### Limit: No Revenue Data

**Trigger**: Questions about financial impact, ROI, revenue
**Agent response**: "I don't have revenue or transaction data. I can show
customer satisfaction metrics, but cannot calculate financial impact."

### Limit: Sparse Verbatims

**Trigger**: Text analysis, sentiment, keyword requests
**Agent response**: "Only {pct}% of records have text comments. Results
may not be representative of all feedback."
```

---

## Can/Cannot Lists

Provide explicit capability boundaries:

```markdown
### What You CAN Answer

- Average rating/NPS by shop, region, segment
- Feedback volume trends over time
- Top/bottom performing shops
- Distribution of scores
- Response rates by channel

### What You CANNOT Answer

- Revenue impact of customer satisfaction
- Customer lifetime value by segment
- Demographic breakdowns
- Competitor benchmarks
- Predictive churn models (no customer-level data)
```

---

## Completeness Matrix

Show coverage visually:

```markdown
### Data Coverage Matrix

| Dimension | Google Reviews | SMS Surveys |
|-----------|---------------|-------------|
| Has shop_id | 100% | 64% |
| Has rating/NPS | 99.8% | 100% |
| Has verbatim | 22% | 15% |
| Has date | 100% | 100% |
| Has channel | N/A | 100% |
| Has language | 100% | 100% |
```

---

## Temporal Boundaries

Always document time ranges:

```markdown
### Temporal Boundaries

| Table | Column | Start | End | Notes |
|-------|--------|-------|-----|-------|
| fact_google_reviews | review_date | 2023-01-01 | 2024-06-30 | 18 months |
| fact_sms_surveys | survey_date | 2024-01-01 | 2024-06-30 | 6 months |
| dim_shops | — | Snapshot | 2024-06-15 | Point-in-time |

**Important**: Google Reviews and SMS Surveys only overlap for 6 months
(2024-01 to 2024-06). Year-over-year comparisons only possible for Google Reviews.
```

---

## Red Flags for Agent

Teach the agent to recognize dangerous queries:

```markdown
### Query Red Flags

| If user asks for... | Watch out for... |
|---------------------|------------------|
| "All customer feedback" | SMS 36% unlinked |
| "Revenue correlation" | No revenue data exists |
| "Year over year SMS" | Only 6 months of SMS data |
| "Customer segments" | No demographic data |
| "Text sentiment analysis" | 78% verbatims empty |
```

---

## Anti-Patterns

### 1. Hiding Limits in Footnotes

**Bad**: Provide results first, mention limits in small print at end.

**Good**: State limits upfront when they affect the answer.

### 2. Overstating Coverage

**Bad**: "Analysis of customer feedback..."

**Good**: "Analysis of 64% of SMS surveys (those linked to shops)..."

### 3. Silent Data Loss

**Bad**: Use INNER JOIN without mentioning excluded records.

**Good**: State how many records excluded and why.

---

## Output Checklist

When documenting limits:

- [ ] Every coverage gap has record counts
- [ ] Every limit has an "impact" description
- [ ] Every significant limit has agent response template
- [ ] CAN/CANNOT lists are explicit
- [ ] Temporal boundaries are documented
- [ ] Red flags listed for dangerous queries
- [ ] Coverage matrix shows completeness by dimension
