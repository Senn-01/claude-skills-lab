---
phase: llm
project: orange-cx-intelligence
date: 2025-12-22T14:00:00Z
status: complete
source_phases:
  - data-understand: ai-docs/data-understand-orange-cx-intelligence.md
  - data-explore: ai-docs/data-explore-orange-cx-intelligence.md
  - data-clean: ai-docs/data-clean-orange-cx-intelligence.md
  - data-validate: ai-docs/data-validate-orange-cx-intelligence.md
quality_score: 99.9%
---

# Data Context: Orange CX Intelligence

## TL;DR

You have **customer feedback data for Orange Belgium retail shops**:
- **161 shops** (dim_shops) — retail locations with management hierarchy
- **1,815 Google reviews** (fact_google_reviews) — star ratings + text + AI responses
- **5,268 SMS surveys** (fact_sms_surveys) — post-transaction satisfaction scores

**You CAN answer**: Ratings/NPS by shop, region, segment, channel. Trends over time. Top/bottom performers. Verbatim themes (limited).

**You CANNOT answer**: Revenue impact. Customer demographics. 36% of SMS surveys (unlinked to shops). Competitor benchmarks.

---

## Schema Overview

### dim_shops (161 rows) — One row per retail location

| Column | Type | Meaning | Example | Notes |
|--------|------|---------|---------|-------|
| shop_id | STRING | Primary key (MongoDB ObjectId) | `6669610334fb243c680a7680` | UUID format |
| mobis_code | STRING | Internal shop identifier | `MOBIS499` | Always UPPERCASE |
| shop_name | STRING | Display name | `ORANGE SHOP WATERLOO` | |
| city | STRING | City name | `Waterloo` | |
| address | STRING | Street address | `Chaussée de Bruxelles 123` | |
| zipcode | STRING | Belgian postal code | `1410` | Maps to language |
| macro_segment | STRING | Business model | `Orange Shops` | Enum: Orange Shops, DISTRIBUTORS, Retail Others, Retail Carrefour |
| new_mainchain | STRING | Chain/partner name | `MOBISTAR OWNED SHOPS` | |
| manager_name | STRING | Shop manager | `Jean Dupont` | 15% populated |
| manager_email | STRING | Manager email | `jean@orange.be` | 14% populated |
| kam_name | STRING | Key Account Manager | `Marie Martin` | 85% populated |
| kam_email | STRING | KAM email | `marie@orange.be` | 85% populated |
| rsm_name | STRING | Regional Sales Manager | | Sparse |
| rsm_email | STRING | RSM email | | Sparse |
| language | STRING | Primary language | `FR` | Enum: NL, FR, BI. Inferred from zipcode |

### fact_google_reviews (1,815 rows) — One row per Google review

| Column | Type | Meaning | Example | Notes |
|--------|------|---------|---------|-------|
| review_id | STRING | Primary key | `ChZDSUhNMGd...` | 24 duplicates exist |
| shop_id | STRING | FK → dim_shops | `668c003316119aced8009790` | 100% populated |
| review_timestamp | TIMESTAMP | When review posted | `2025-07-15T14:30:00Z` | UTC. Range: 2025-07 to 2025-11 |
| rating | INT | Star rating | `4` | Range: 1-5. 3 NULLs exist |
| verbatim | STRING | Review text (translated) | `Great service!` | 78% NULL |
| client_name | STRING | Reviewer name | `John D.` | PII |
| response_timestamp | TIMESTAMP | When AI responded | `2025-07-16T09:00:00Z` | 52% populated |
| ai_response | STRING | Generated response | `Thank you for...` | Multilingual FR/NL |
| is_corrected | BOOLEAN | Manually corrected? | `false` | 0.05% true |
| correction_text | STRING | Manual correction | | 99.95% NULL |
| duplicate_flag | STRING | Source flag | `ok` | |

### fact_sms_surveys (5,268 rows) — One row per SMS survey response

| Column | Type | Meaning | Example | Notes |
|--------|------|---------|---------|-------|
| survey_id | STRING | Primary key | `R_3nHJ7kM...` | Unique |
| shop_id | STRING | FK → dim_shops | `6669610334fb243c680a7680` | **64% populated, 36% NULL** |
| mobis_code | STRING | Extracted shop code | `MOBIS344` | 87% populated |
| interaction_date | DATE | Transaction date | `2025-11-15` | Range: 2025-08-25 to 2025-11-27 |
| response_date | DATE | Survey completed | `2025-11-16` | Range: 2025-11-01 to 2025-11-30 |
| rating | INT | Satisfaction score | `5` | Range: 1-5. Mean: 4.64 |
| verbatim | STRING | Free-text comment | `Very helpful staff` | **78% NULL** |
| vendor_id | STRING | Staff ID | `V12345` | |
| audience_type | STRING | Customer type | `SUBSCRIPTION` | Enum: SUBSCRIPTION, Prospect |
| customer_type | STRING | Segment | `SUBSCRIBERS` | Enum: SUBSCRIBERS, FIRMS, N/A |
| channel | STRING | Distribution channel | `OSO` | Enum: OSO (82%), TZ Carrefour (18%) |
| case_type | STRING | Transaction type | `New Activation` | ~15 values |
| case_level_1 | STRING | Category hierarchy | | 68% NULL |
| case_level_2 | STRING | Category hierarchy | | 68% NULL |
| case_level_3 | STRING | Category hierarchy | | 68% NULL |
| source_system | STRING | Source | `Activation` | Enum: Activation, Purchase |
| is_mappable | BOOLEAN | Linked to shop? | `true` | 64% true |

---

## Relationships

```
                         dim_shops
                         ─────────
                         shop_id (PK)
                         mobis_code (unique)
                              │
         ┌────────────────────┴────────────────────┐
         │                                         │
         ▼                                         ▼
   fact_google_reviews                      fact_sms_surveys
   ────────────────────                     ────────────────────
   shop_id (FK) ────────────────────────►   shop_id (FK, nullable)
   100% linked                              64% linked, 36% NULL
                                            mobis_code (alternate key)
```

### Join Cardinality

| From | To | Type | Coverage |
|------|----|------|----------|
| dim_shops → fact_google_reviews | 1:N | 145 of 161 shops have reviews (90%) |
| dim_shops → fact_sms_surveys | 1:N | 133 of 161 shops have surveys (83%) |
| fact_sms_surveys.shop_id | nullable | 36% NULL (1,905 records unlinked) |

---

## Data Limits

> **IMPORTANT**: These limits affect what questions can be answered. You MUST mention relevant limits when answering questions.

### Coverage Limits

| Limitation | Affected Records | Impact | Agent Must Say |
|------------|------------------|--------|----------------|
| 36% SMS unlinked | 1,905 of 5,268 | Cannot join to dim_shops | "This covers 64% of SMS surveys (those linked to shops)" |
| 28 unknown MOBIS | 1,218 SMS | Shop not in master data | "Some surveys reference shops not in our master data" |
| 78% verbatims empty | 4,102 of 5,268 SMS | Limited text analysis | "Most surveys don't have text comments" |
| 78% review text empty | 1,416 of 1,815 reviews | Limited text analysis | "Most reviews don't have text comments" |

### What You CAN Answer

- Average rating/NPS by shop, region, segment, channel
- Rating distribution (1-5 stars, NPS score)
- Feedback volume trends over time (Nov 2025 for SMS, Jul-Nov 2025 for reviews)
- Top/bottom performing shops (by average rating)
- Feedback by transaction type (case_type)
- Shop comparisons within same segment
- AI response patterns and correction rates

### What You CANNOT Answer

| Question Type | Why Not | What to Say |
|---------------|---------|-------------|
| "Revenue impact of low ratings" | No revenue data | "I can show satisfaction metrics but not financial impact" |
| "Customer demographics" | No age/gender data | "No demographic data available" |
| "Full SMS analysis by shop" | 36% unlinked | "Can only analyze 64% of SMS when grouping by shop. Alternatively, analyze by channel or MOBIS code." |
| "Year-over-year trends" | Only 2025 data | "Data only covers 2025 (Jul-Nov for reviews, Nov for SMS)" |
| "Competitor comparison" | No external data | "Only internal Orange shop data available" |

---

## Query Patterns

### Pattern 1: Shop Performance Ranking

**For questions like**: "Which shops have the best/worst ratings?"

```sql
SELECT
    s.shop_name,
    s.city,
    s.macro_segment,
    ROUND(AVG(r.rating), 2) as avg_rating,
    COUNT(*) as review_count
FROM dim_shops s
JOIN fact_google_reviews r ON s.shop_id = r.shop_id
WHERE r.rating IS NOT NULL  -- 3 nulls exist
GROUP BY s.shop_id, s.shop_name, s.city, s.macro_segment
HAVING COUNT(*) >= 5  -- Statistical significance
ORDER BY avg_rating DESC
```

**Caveat**: "Rankings based on shops with 5+ reviews for statistical reliability."

### Pattern 2: NPS by Segment

**For questions like**: "What's the NPS by business type?"

```sql
-- NPS = % Promoters (4-5) - % Detractors (1-2) for 1-5 scale
-- Adjust: 5=promoter, 1-3=detractor, 4=passive
SELECT
    s.macro_segment,
    COUNT(*) as responses,
    ROUND(100.0 * SUM(CASE WHEN f.rating = 5 THEN 1 ELSE 0 END) / COUNT(*), 1) as pct_promoters,
    ROUND(100.0 * SUM(CASE WHEN f.rating <= 3 THEN 1 ELSE 0 END) / COUNT(*), 1) as pct_detractors,
    ROUND(
        100.0 * SUM(CASE WHEN f.rating = 5 THEN 1 ELSE 0 END) / COUNT(*) -
        100.0 * SUM(CASE WHEN f.rating <= 3 THEN 1 ELSE 0 END) / COUNT(*),
        1
    ) as nps
FROM fact_sms_surveys f
JOIN dim_shops s ON f.shop_id = s.shop_id
WHERE f.shop_id IS NOT NULL  -- Exclude 36% unlinked
GROUP BY s.macro_segment
ORDER BY nps DESC
```

**Caveat**: "This covers 64% of SMS surveys (3,363 of 5,268). Surveys without shop links are excluded."

### Pattern 3: Time Trend

**For questions like**: "How has feedback changed over time?"

```sql
SELECT
    DATE_TRUNC(review_timestamp, WEEK) as week,
    COUNT(*) as review_count,
    ROUND(AVG(rating), 2) as avg_rating
FROM fact_google_reviews
WHERE rating IS NOT NULL
GROUP BY 1
ORDER BY 1
```

**Caveat**: "Google Reviews data covers July-November 2025. SMS surveys only November 2025."

### Pattern 4: Channel Comparison

**For questions like**: "How do OSO shops compare to Carrefour?"

```sql
SELECT
    f.channel,
    COUNT(*) as surveys,
    ROUND(AVG(f.rating), 2) as avg_rating,
    ROUND(100.0 * SUM(CASE WHEN f.rating = 5 THEN 1 ELSE 0 END) / COUNT(*), 1) as pct_5_star
FROM fact_sms_surveys f
GROUP BY f.channel
```

**Note**: This query uses ALL SMS data (no shop join required).

### Pattern 5: Verbatim Text Analysis

**For questions like**: "What are customers complaining about?"

```sql
SELECT
    s.shop_name,
    f.verbatim,
    f.rating,
    f.response_date
FROM fact_sms_surveys f
LEFT JOIN dim_shops s ON f.shop_id = s.shop_id
WHERE f.verbatim IS NOT NULL
  AND f.verbatim != ''
  AND f.rating <= 3  -- Focus on negative feedback
ORDER BY f.response_date DESC
LIMIT 50
```

**Caveat**: "Only 22% of surveys have text comments. Results may not be representative."

---

## Anti-Patterns (DO NOT USE)

### Anti-Pattern 1: INNER JOIN on SMS Surveys

```sql
-- WRONG: Silently drops 36% of SMS data!
SELECT s.shop_name, AVG(f.rating)
FROM fact_sms_surveys f
INNER JOIN dim_shops s ON f.shop_id = s.shop_id
GROUP BY s.shop_name
```

```sql
-- RIGHT: Use LEFT JOIN and acknowledge NULL shop_id
SELECT
    COALESCE(s.shop_name, CONCAT('Unlinked (', f.mobis_code, ')')) as shop,
    AVG(f.rating) as avg_rating,
    SUM(CASE WHEN s.shop_id IS NULL THEN 1 ELSE 0 END) as unlinked_count
FROM fact_sms_surveys f
LEFT JOIN dim_shops s ON f.shop_id = s.shop_id
GROUP BY 1
```

### Anti-Pattern 2: Ignoring NULL Ratings

```sql
-- WRONG: AVG ignores NULLs silently
SELECT AVG(rating) FROM fact_google_reviews
-- User thinks this is all reviews, but 3 are excluded
```

```sql
-- RIGHT: Acknowledge NULLs
SELECT
    COUNT(*) as total_reviews,
    COUNT(rating) as rated_reviews,
    AVG(rating) as avg_rating
FROM fact_google_reviews
-- Makes NULL count explicit
```

### Anti-Pattern 3: Assuming Review ID is Unique

```sql
-- WRONG: 24 duplicate review_ids exist
SELECT * FROM fact_google_reviews WHERE review_id = 'xyz'
-- May return multiple rows
```

```sql
-- RIGHT: Dedupe if needed
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY review_id ORDER BY review_timestamp DESC) as rn
    FROM fact_google_reviews
) WHERE rn = 1
```

---

## Domain Glossary

### Core Metrics

| Term | Definition | SQL |
|------|------------|-----|
| Rating | Satisfaction score | `rating` (1-5 scale) |
| NPS | Net Promoter Score | See Pattern 2 calculation |
| Promoter | High satisfaction (5) | `WHERE rating = 5` |
| Detractor | Low satisfaction (1-3) | `WHERE rating <= 3` |
| Passive | Neutral (4) | `WHERE rating = 4` |
| Verbatim | Free-text customer comment | `verbatim` column |

### Entity Types

| Term | Definition | SQL |
|------|------------|-----|
| Shop | Retail location | `dim_shops` table |
| MOBIS | Internal shop ID | `mobis_code` column (format: MOBIS###) |
| Orange Shop | Company-owned retail | `macro_segment = 'Orange Shops'` |
| Distributor | Partner-owned shop | `macro_segment = 'DISTRIBUTORS'` |
| OSO | Orange Shop Owned (channel) | `channel = 'OSO'` |
| TZ Carrefour | Traffic Zone Carrefour | `channel = 'TZ Carrefour'` |
| KAM | Key Account Manager | `kam_name`, `kam_email` |
| RSM | Regional Sales Manager | `rsm_name`, `rsm_email` |

### Languages

| Term | Definition | SQL |
|------|------------|-----|
| French-speaking | Wallonia region | `language = 'FR'` |
| Dutch-speaking | Flanders region | `language = 'NL'` |
| Bilingual | Brussels region | `language = 'BI'` |

### Synonyms (User → System)

| User Says | Means | SQL |
|-----------|-------|-----|
| "unhappy customer" | Detractor | `rating <= 3` |
| "happy customer" | Promoter | `rating = 5` |
| "problem shop" | Low-rated shop | `AVG(rating) < 3.5` |
| "best shop" | High-rated shop | `AVG(rating) >= 4.5` |
| "French region" | Wallonia | `language = 'FR'` |
| "Flemish region" | Flanders | `language = 'NL'` |
| "complaints" | Negative verbatims | `verbatim IS NOT NULL AND rating <= 3` |
| "feedback volume" | Count of responses | `COUNT(*)` |

---

## Temporal Boundaries

| Table | Column | Start | End | Span |
|-------|--------|-------|-----|------|
| fact_google_reviews | review_timestamp | 2025-07-01 | 2025-11-30 | 5 months |
| fact_sms_surveys | response_date | 2025-11-01 | 2025-11-30 | 1 month |
| fact_sms_surveys | interaction_date | 2025-08-25 | 2025-11-27 | 3 months |
| dim_shops | — | Snapshot | 2025-12-22 | Point-in-time |

**Important**:
- Google Reviews and SMS Surveys only overlap for November 2025
- Year-over-year comparisons NOT possible (data starts mid-2025)
- SMS surveys limited to November 2025 responses

---

## Data Quality Notes

| Issue | Scope | Handling |
|-------|-------|----------|
| 24 duplicate review_ids | 1.3% of reviews | Dedupe in query if needed |
| 3 NULL ratings | 0.17% of reviews | Filter with `WHERE rating IS NOT NULL` |
| 30 pre-July timestamps | 1.7% of reviews | Historical reviews, valid data |
| 2 temporal violations | 0.1% of reviews | response_timestamp before review_timestamp |

**Overall Quality**: 99.9% certified (threshold 95%)

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────┐
│ ORANGE CX INTELLIGENCE - QUICK REFERENCE                        │
├─────────────────────────────────────────────────────────────────┤
│ TABLES:                                                         │
│   dim_shops             161 rows    Shop master data            │
│   fact_google_reviews   1,815 rows  Google Reviews (Jul-Nov)    │
│   fact_sms_surveys      5,268 rows  SMS Surveys (Nov only)      │
├─────────────────────────────────────────────────────────────────┤
│ KEY LIMITS:                                                     │
│   • 36% of SMS unlinked to shops (use LEFT JOIN!)              │
│   • 78% of verbatims empty (limited text analysis)              │
│   • No revenue data, no demographics                            │
├─────────────────────────────────────────────────────────────────┤
│ JOIN KEYS:                                                      │
│   dim_shops.shop_id ← fact_google_reviews.shop_id (100%)       │
│   dim_shops.shop_id ← fact_sms_surveys.shop_id (64%)           │
├─────────────────────────────────────────────────────────────────┤
│ RATINGS:                                                        │
│   • Scale: 1-5 stars                                            │
│   • Promoter: 5 | Passive: 4 | Detractor: 1-3                  │
│   • SMS mean: 4.64 (highly positive skew)                       │
└─────────────────────────────────────────────────────────────────┘
```
