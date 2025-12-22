# Query Pattern Templates

## The Goal

Provide proven SQL patterns that:
1. Work correctly on THIS specific data
2. Handle known edge cases (NULLs, joins, filters)
3. Include appropriate caveats
4. Can be adapted for similar questions

---

## Pattern Structure

Each pattern should include:

```markdown
### Pattern: {Descriptive Name}

**User might ask**: "{natural language question}"

**Key considerations**:
- {edge case 1}
- {edge case 2}

**SQL**:
```sql
-- Comment explaining the query
SELECT ...
```

**Caveat to include**: "{what agent should tell user}"
```

---

## Core Pattern Types

### 1. Aggregation by Dimension

```markdown
### Pattern: Aggregate Metric by Dimension

**User might ask**: "Show me average {metric} by {dimension}"

**Template**:
```sql
SELECT
    d.{dimension_col},
    COUNT(*) as record_count,
    ROUND(AVG(f.{metric_col}), 2) as avg_{metric}
FROM {fact_table} f
JOIN {dim_table} d ON f.{join_key} = d.{join_key}
GROUP BY d.{dimension_col}
HAVING COUNT(*) >= {min_sample}  -- Statistical significance
ORDER BY avg_{metric} DESC
```

**Considerations**:
- HAVING clause prevents misleading small-sample averages
- Always include record_count for context
- JOIN type matters: INNER excludes unmatched, LEFT preserves all
```

### 2. Top/Bottom N

```markdown
### Pattern: Top/Bottom Performers

**User might ask**: "Which {entities} have the best/worst {metric}?"

**Template**:
```sql
SELECT
    d.{entity_name},
    d.{entity_attributes},
    ROUND(AVG(f.{metric}), 2) as avg_metric,
    COUNT(*) as sample_size
FROM {fact_table} f
JOIN {dim_table} d ON f.{join_key} = d.{join_key}
GROUP BY d.{entity_id}, d.{entity_name}, d.{entity_attributes}
HAVING COUNT(*) >= {min_sample}
ORDER BY avg_metric {DESC|ASC}
LIMIT {N}
```

**Considerations**:
- Always require minimum sample size
- Include sample_size in output for credibility
- Consider: should ties be included? (RANK vs LIMIT)
```

### 3. Time Series Trends

```markdown
### Pattern: Metric Over Time

**User might ask**: "How has {metric} changed over time?"

**Template**:
```sql
SELECT
    DATE_TRUNC('{granularity}', f.{date_col}) as period,
    COUNT(*) as volume,
    ROUND(AVG(f.{metric}), 2) as avg_metric
FROM {fact_table} f
WHERE f.{date_col} BETWEEN '{start_date}' AND '{end_date}'
GROUP BY 1
ORDER BY 1
```

**Granularity options**: day, week, month, quarter, year

**Considerations**:
- Check temporal boundaries before querying
- Note gaps in time series
- Consider seasonality
```

### 4. Distribution Analysis

```markdown
### Pattern: Value Distribution

**User might ask**: "What's the distribution of {metric}?"

**Template**:
```sql
SELECT
    f.{metric_col} as value,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as pct
FROM {fact_table} f
WHERE f.{metric_col} IS NOT NULL
GROUP BY f.{metric_col}
ORDER BY f.{metric_col}
```

**For continuous metrics (buckets)**:
```sql
SELECT
    CASE
        WHEN {metric} < 3 THEN 'Low (1-2)'
        WHEN {metric} < 4 THEN 'Medium (3)'
        WHEN {metric} >= 4 THEN 'High (4-5)'
    END as bucket,
    COUNT(*) as count
FROM {fact_table}
GROUP BY 1
ORDER BY 1
```
```

### 5. Segment Comparison

```markdown
### Pattern: Compare Segments

**User might ask**: "How does {metric} differ between {segment_a} and {segment_b}?"

**Template**:
```sql
SELECT
    d.{segment_col},
    COUNT(*) as n,
    ROUND(AVG(f.{metric}), 2) as avg_metric,
    ROUND(STDDEV(f.{metric}), 2) as stddev_metric
FROM {fact_table} f
JOIN {dim_table} d ON f.{join_key} = d.{join_key}
GROUP BY d.{segment_col}
ORDER BY avg_metric DESC
```

**Considerations**:
- Include stddev to show variance within segments
- Note sample size differences
- Consider statistical significance for small segments
```

---

## Anti-Patterns Section

Always include what NOT to do:

```markdown
## Anti-Patterns (DO NOT USE)

### Anti-Pattern: Silent Data Loss with INNER JOIN

**Wrong**:
```sql
-- This silently drops 36% of SMS data!
SELECT s.shop_name, AVG(f.nps_score)
FROM fact_sms_surveys f
INNER JOIN dim_shops s ON f.shop_id = s.shop_id
GROUP BY s.shop_name
```

**Right**:
```sql
-- Use LEFT JOIN and acknowledge excluded records
SELECT
    COALESCE(s.shop_name, CONCAT('Unlinked (', f.mobis_code, ')')) as shop,
    AVG(f.nps_score) as avg_nps,
    COUNT(*) as n,
    SUM(CASE WHEN s.shop_id IS NULL THEN 1 ELSE 0 END) as unlinked_count
FROM fact_sms_surveys f
LEFT JOIN dim_shops s ON f.shop_id = s.shop_id
GROUP BY 1
```

### Anti-Pattern: Averaging Averages

**Wrong**:
```sql
-- Averaging pre-computed averages ignores sample sizes
SELECT AVG(shop_avg_rating)
FROM (
    SELECT shop_id, AVG(rating) as shop_avg_rating
    FROM fact_reviews
    GROUP BY shop_id
)
```

**Right**:
```sql
-- Calculate from raw data
SELECT AVG(rating) FROM fact_reviews
```

### Anti-Pattern: Ignoring NULLs in Counts

**Wrong**:
```sql
-- COUNT(*) includes NULLs, COUNT(col) excludes them
SELECT COUNT(*) as total, AVG(rating) as avg
FROM reviews
-- If 100 rows but 10 NULL ratings: count=100, avg based on 90
```

**Right**:
```sql
SELECT
    COUNT(*) as total_records,
    COUNT(rating) as rated_records,
    AVG(rating) as avg_rating
FROM reviews
```
```

---

## Domain-Specific Patterns

Include patterns for common business metrics:

```markdown
## Business Metric Patterns

### NPS Calculation

```sql
-- Net Promoter Score = % Promoters - % Detractors
SELECT
    segment,
    COUNT(*) as responses,
    ROUND(100.0 * SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END) / COUNT(*), 1) as pct_promoters,
    ROUND(100.0 * SUM(CASE WHEN nps_score <= 6 THEN 1 ELSE 0 END) / COUNT(*), 1) as pct_detractors,
    ROUND(
        100.0 * SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END) / COUNT(*) -
        100.0 * SUM(CASE WHEN nps_score <= 6 THEN 1 ELSE 0 END) / COUNT(*),
        1
    ) as nps
FROM fact_surveys
GROUP BY segment
```

### Response Rate

```sql
-- If you have sent vs received counts
SELECT
    period,
    surveys_sent,
    surveys_received,
    ROUND(100.0 * surveys_received / NULLIF(surveys_sent, 0), 1) as response_rate_pct
FROM survey_metrics
```

### Year-over-Year Comparison

```sql
SELECT
    current.period,
    current.metric as current_value,
    previous.metric as previous_value,
    ROUND(100.0 * (current.metric - previous.metric) / NULLIF(previous.metric, 0), 1) as yoy_change_pct
FROM metrics current
LEFT JOIN metrics previous
    ON current.period = DATE_ADD(previous.period, INTERVAL 1 YEAR)
```
```

---

## Query Building Checklist

When generating queries:

- [ ] Chose correct JOIN type (INNER vs LEFT)
- [ ] Handled NULL values explicitly
- [ ] Included record counts for context
- [ ] Applied minimum sample size where needed
- [ ] Checked temporal boundaries
- [ ] Used appropriate aggregation level
- [ ] Included caveat for agent response
- [ ] Avoided anti-patterns

---

## Output Format

In the final LLM context document, present patterns like:

```markdown
## Query Patterns

### Pattern 1: Shop Performance Ranking

**For questions like**: "Which shops have the best ratings?"

```sql
SELECT
    s.shop_name,
    s.city,
    s.macro_segment,
    ROUND(AVG(r.rating), 2) as avg_rating,
    COUNT(*) as review_count
FROM dim_shops s
JOIN fact_google_reviews r ON s.shop_id = r.shop_id
GROUP BY 1, 2, 3
HAVING COUNT(*) >= 5
ORDER BY avg_rating DESC
```

**Caveat**: "Rankings based on shops with 5+ reviews for statistical reliability."

---

### Anti-Pattern: DON'T Use INNER JOIN on SMS

```sql
-- WRONG: Silently drops 36% of data
SELECT * FROM fact_sms_surveys f
INNER JOIN dim_shops s ON f.shop_id = s.shop_id

-- RIGHT: Preserve all data, handle NULLs
SELECT * FROM fact_sms_surveys f
LEFT JOIN dim_shops s ON f.shop_id = s.shop_id
```
```
