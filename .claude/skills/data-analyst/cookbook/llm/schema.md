# Schema Documentation Patterns

## The Goal

Document schema so an LLM can:
1. Know exactly what columns exist (no hallucination)
2. Understand what each column MEANS (semantics)
3. Know data types and valid values (constraints)
4. Understand row-level grain (what one row represents)

---

## Table Documentation Pattern

### Template

```markdown
### {table_name} ({row_count} rows) — {grain description}

| Column | Type | Meaning | Example | Notes |
|--------|------|---------|---------|-------|
| col_a | STRING | Primary key | "abc-123" | UUID format |
| col_b | INTEGER | Business metric | 42 | Range: 0-100 |
| col_c | STRING | Category | "TYPE_A" | Enum: TYPE_A, TYPE_B |
| col_d | TIMESTAMP | Event time | 2024-01-15 | UTC timezone |
```

### Key Elements

1. **Row count**: Gives scale context
2. **Grain description**: "One row = one {thing}"
3. **Type**: Actual SQL type (STRING, INTEGER, FLOAT, TIMESTAMP, BOOLEAN)
4. **Meaning**: Business definition, not technical
5. **Example**: Real value from data
6. **Notes**: Constraints, quirks, warnings

---

## Grain Descriptions

The grain tells the LLM what one row represents. This is critical for correct aggregation.

### Good Grain Descriptions

```
dim_shops (161 rows) — One row per retail location
fact_google_reviews (1,815 rows) — One row per Google review
fact_sms_surveys (5,268 rows) — One row per SMS survey response
dim_date (365 rows) — One row per calendar day
fact_transactions (1.2M rows) — One row per line item (not per order)
```

### Why Grain Matters

Without grain, LLM might:
- COUNT(*) when it should COUNT(DISTINCT customer_id)
- Double-count when joining one-to-many
- Aggregate at wrong level

With grain, LLM knows:
- "fact_transactions is line items, so COUNT(*) = items, not orders"
- "To count orders, use COUNT(DISTINCT order_id)"

---

## Column Type Patterns

### Primary Keys

```
| shop_id | STRING | Primary key - unique shop identifier | "abc-123" | UUID, never NULL |
```

Mark PKs explicitly. Note format (UUID, integer, composite).

### Foreign Keys

```
| shop_id | STRING | FK → dim_shops.shop_id | "abc-123" | 64% populated, 36% NULL |
```

Always note:
- Which table it references
- Population rate (especially if partial)

### Enums/Categories

```
| macro_segment | STRING | Business model | "FRANCHISE" | Enum: FRANCHISE, OWN, CORNER |
```

List ALL valid values. LLM needs to know valid WHERE clause values.

### Numeric Ranges

```
| nps_score | INTEGER | Net Promoter Score | 7 | Range: 0-10 |
| rating | INTEGER | Star rating | 4 | Range: 1-5 |
| pct_complete | FLOAT | Completion percentage | 0.85 | Range: 0.0-1.0 |
```

Always specify min/max. Prevents impossible filters.

### Dates/Times

```
| review_date | DATE | When review was posted | 2024-03-15 | Range: 2023-01-01 to 2024-06-30 |
| created_at | TIMESTAMP | Record creation time | 2024-03-15T14:30:00Z | UTC timezone |
```

Note:
- Date vs Timestamp
- Timezone (UTC assumed unless stated)
- Data range (temporal boundaries)

### Free Text

```
| verbatim | STRING | Customer comment text | "Great service!" | 78% NULL, avg 45 chars |
```

Note sparsity and typical length.

---

## Relationship Documentation

### Text-Based ERD

```markdown
## Relationships

```
dim_shops.shop_id ←─┬── fact_google_reviews.shop_id (100% populated)
                    └── fact_sms_surveys.shop_id (64% populated)

dim_shops.mobis_code ←── fact_sms_surveys.mobis_code (100% populated)
```
```

### Join Cardinality

Always note:
- **1:1** — Each row matches exactly one
- **1:N** — One dimension row, many fact rows
- **N:M** — Many-to-many (usually needs bridge table)

```markdown
### Cardinality

| From | To | Type | Notes |
|------|----|------|-------|
| dim_shops → fact_google_reviews | 1:N | One shop has many reviews |
| dim_shops → fact_sms_surveys | 1:N | One shop has many surveys |
| fact_sms_surveys.shop_id | Optional | 36% NULL |
```

---

## Semantic Annotations

### Business Definitions (not technical)

**Bad**: "nps_score: integer column"
**Good**: "nps_score: Net Promoter Score (0-10), where 9-10 = promoter, 7-8 = passive, 0-6 = detractor"

**Bad**: "created_at: timestamp"
**Good**: "created_at: When customer submitted the survey (UTC)"

### Derivation Notes

If a column was computed/inferred:

```
| language | STRING | Primary language | "FR" | Inferred from zipcode (not original data) |
```

LLM should know what's measured vs derived.

### Business Rules Embedded in Data

```
| macro_segment | STRING | Business model | "FRANCHISE" | Note: "CLOSED" means defunct shop, filter out for active analysis |
```

---

## Anti-Patterns to Avoid

### 1. Generic Column Names Without Context

**Bad**:
```
| id | STRING | Identifier | |
| type | STRING | Type | |
| value | FLOAT | Value | |
```

**Good**:
```
| shop_id | STRING | Unique shop identifier (PK) | "abc-123" | UUID format |
| shop_type | STRING | Ownership model | "FRANCHISE" | Enum: FRANCHISE, OWN, CORNER |
| nps_score | INTEGER | Net Promoter Score | 8 | Range: 0-10 |
```

### 2. Missing NULL Information

**Bad**:
```
| shop_id | STRING | FK to shops | |
```

**Good**:
```
| shop_id | STRING | FK → dim_shops | | 64% populated, 36% NULL |
```

### 3. Implicit Enums

**Bad**:
```
| status | STRING | Status | |
```

**Good**:
```
| status | STRING | Order status | "SHIPPED" | Enum: PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED |
```

---

## Schema Extraction Checklist

When documenting schema:

- [ ] Every table has row count
- [ ] Every table has grain description
- [ ] Every column has type
- [ ] Every column has business meaning
- [ ] Every column has example value
- [ ] PKs marked explicitly
- [ ] FKs note target table AND population rate
- [ ] Enums list ALL valid values
- [ ] Numerics have min/max ranges
- [ ] Dates have temporal boundaries
- [ ] NULL rates noted for nullable columns
- [ ] Derived columns marked as derived

---

## Output Format

Combine into single Schema Overview section:

```markdown
## Schema Overview

### dim_shops (161 rows) — One row per retail location

| Column | Type | Meaning | Example | Notes |
|--------|------|---------|---------|-------|
| shop_id | STRING | Primary key | "abc-123" | UUID |
| mobis_code | STRING | Business system ID | "MOBIS467" | UPPERCASE only |
| shop_name | STRING | Display name | "Orange Liège" | |
| zipcode | STRING | Belgian postal code | "4000" | Maps to language |
| language | STRING | Primary language | "FR" | Inferred from zip |
| macro_segment | STRING | Business model | "FRANCHISE" | Enum: FRANCHISE, OWN, CORNER |

### fact_google_reviews (1,815 rows) — One row per Google review

| Column | Type | Meaning | Example | Notes |
|--------|------|---------|---------|-------|
| review_id | STRING | Primary key | "rev-456" | Unique |
| shop_id | STRING | FK → dim_shops | "abc-123" | 100% populated |
| rating | INTEGER | Star rating | 4 | Range: 1-5 |
| review_date | DATE | When posted | 2024-03-15 | Range: 2023-01 to 2024-06 |
| verbatim | STRING | Review text | "Great!" | 78% NULL |

## Relationships

```
dim_shops.shop_id ←─┬── fact_google_reviews.shop_id (100%)
                    └── fact_sms_surveys.shop_id (64%)
```
```
