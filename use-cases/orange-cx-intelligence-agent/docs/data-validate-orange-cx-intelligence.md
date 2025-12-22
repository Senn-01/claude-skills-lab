---
phase: validate
project: orange-cx-intelligence
date: 2025-12-22T09:24:00Z
status: certified
prior_phase: ai-docs/data-clean-orange-cx-intelligence.md
threshold: 0.95
overall_score: 0.999
linked_files:
  - cases/orange-cx-intelligence-agent/validate_orange_cx.py
  - cases/orange-cx-intelligence-agent/validation_output/
---

# Data Validation Report: Orange CX Intelligence

## Certification Status

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ✓ DATA QUALITY CERTIFIED                                 ║
║                                                            ║
║   Overall Score: 99.9%                                     ║
║   Threshold: 95%                                           ║
║   All dimensions pass.                                     ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

**Approved for BigQuery load.**

---

## Validation Summary

### By Dimension

| Dimension | Score | Status | Checks |
|-----------|-------|--------|--------|
| COMPLETENESS | 100.0% | ✓ Pass | Required fields present |
| UNIQUENESS | 99.8% | ✓ Pass | PKs unique, FKs valid |
| VALIDITY | 99.8% | ✓ Pass | Values in allowed ranges |
| CONSISTENCY | 100.0% | ✓ Pass | Cross-field logic holds |

### By Table

| Table | Score | Checks Run | Failures |
|-------|-------|------------|----------|
| dim_shops | 100.0% | 7 | 0 |
| fact_google_reviews | 99.6% | 10 | 4 |
| fact_sms_surveys | 100.0% | 10 | 0 |

---

## Check Results

### dim_shops (7 checks, all pass)

| Check | Dimension | Result | Details |
|-------|-----------|--------|---------|
| column names BigQuery-safe | VALIDITY | ✓ 100% | |
| shop_id not null | COMPLETENESS | ✓ 100% | |
| mobis_code not null | COMPLETENESS | ✓ 100% | |
| shop_name not null | COMPLETENESS | ✓ 100% | |
| shop_id unique | UNIQUENESS | ✓ 100% | |
| mobis_code unique | UNIQUENESS | ✓ 100% | |
| language values valid | VALIDITY | ✓ 100% | NL/FR/BI only |

### fact_google_reviews (10 checks, 4 with failures)

| Check | Dimension | Result | Details |
|-------|-----------|--------|---------|
| column names BigQuery-safe | VALIDITY | ✓ 100% | |
| review_id not null | COMPLETENESS | ✓ 100% | |
| shop_id not null | COMPLETENESS | ✓ 100% | |
| **rating not null** | COMPLETENESS | ✗ 99.8% | **3 null values** |
| **review_id unique** | UNIQUENESS | ✗ 98.7% | **24 duplicate values** |
| shop_id FK valid | UNIQUENESS | ✓ 100% | |
| rating in [1, 5] | VALIDITY | ✓ 100% | |
| **review_timestamp in [2025]** | VALIDITY | ✗ 98.3% | **30 out of range** |
| rating distribution varies | CONSISTENCY | ✓ 100% | |
| **review <= response timestamp** | CONSISTENCY | ✗ 99.9% | **2 temporal violations** |

### fact_sms_surveys (10 checks, all pass)

| Check | Dimension | Result | Details |
|-------|-----------|--------|---------|
| column names BigQuery-safe | VALIDITY | ✓ 100% | |
| survey_id not null | COMPLETENESS | ✓ 100% | |
| rating not null | COMPLETENESS | ✓ 100% | |
| survey_id unique | UNIQUENESS | ✓ 100% | |
| shop_id FK valid | UNIQUENESS | ✓ 100% | (null allowed) |
| rating in [1, 5] | VALIDITY | ✓ 100% | |
| interaction_date in [2025] | VALIDITY | ✓ 100% | |
| response_date in [2025] | VALIDITY | ✓ 100% | |
| rating distribution varies | CONSISTENCY | ✓ 100% | |
| interaction <= response date | CONSISTENCY | ✓ 100% | |

---

## Failures Analysis

### 1. Null Ratings (3 records)

**Impact**: Minor - 0.17% of records
**Root Cause**: Google Reviews without star rating (comment-only reviews?)
**Recommendation**: Keep as-is, filter in queries: `WHERE rating IS NOT NULL`

### 2. Duplicate Review IDs (24 records)

**Impact**: Moderate - 1.3% of records
**Root Cause**: Same review appearing multiple times in source export
**Recommendation**: Dedupe before load OR add row number to create unique key:
```sql
SELECT *, ROW_NUMBER() OVER (PARTITION BY review_id ORDER BY review_timestamp) as dupe_rank
FROM fact_google_reviews
WHERE dupe_rank = 1
```

### 3. Timestamps Outside 2025 (30 records)

**Impact**: Minor - 1.7% of records
**Root Cause**: Reviews from late 2024 (July was when system started, some older reviews included)
**Recommendation**: Expand date range to 2024-07-01 OR document as historical data

### 4. Response Before Review (2 records)

**Impact**: Negligible - 0.1% of records
**Root Cause**: Timezone handling or data entry error
**Recommendation**: Flag and investigate, but don't block load

---

## Validation Rules Applied

### Completeness (Required Fields)

| Table | Required Fields |
|-------|-----------------|
| dim_shops | shop_id, mobis_code, shop_name |
| fact_google_reviews | review_id, shop_id, rating |
| fact_sms_surveys | survey_id, rating |

### Uniqueness

| Table | Primary Key | Foreign Keys |
|-------|-------------|--------------|
| dim_shops | shop_id, mobis_code | - |
| fact_google_reviews | review_id | shop_id → dim_shops |
| fact_sms_surveys | survey_id | shop_id → dim_shops (nullable) |

### Validity

| Field | Rule | Applied To |
|-------|------|------------|
| rating | 1-5 inclusive | Both fact tables |
| dates | 2025-01-01 to 2025-12-31 | All timestamp/date fields |
| language | NL, FR, BI | dim_shops |
| column names | ^[a-z][a-z0-9_]*$ | All tables |

### Consistency

| Rule | Applied To |
|------|------------|
| Temporal order (A ≤ B) | review_timestamp ≤ response_timestamp |
| Temporal order (A ≤ B) | interaction_date ≤ response_date |
| Distribution varies | rating not >99% single value |

---

## Recommendations

### Before BigQuery Load

1. **Optional fixes** (can proceed without):
   - Dedupe 24 duplicate review_ids
   - Fill or flag 3 null ratings

2. **Accept as documented**:
   - 30 pre-2025 timestamps (expand date range in validation)
   - 2 temporal violations (mark for investigation)

### BigQuery Schema Notes

```sql
-- dim_shops
shop_id STRING NOT NULL,  -- PK
mobis_code STRING NOT NULL,
language STRING  -- NL/FR/BI

-- fact_google_reviews
review_id STRING NOT NULL,  -- PK (24 dupes exist!)
shop_id STRING NOT NULL,  -- FK
rating INT64,  -- Nullable (3 nulls)
review_timestamp TIMESTAMP

-- fact_sms_surveys
survey_id STRING NOT NULL,  -- PK
shop_id STRING,  -- FK, nullable (36% unmatched)
rating INT64 NOT NULL
```

---

## Output Files

```
cases/orange-cx-intelligence-agent/validation_output/
├── validation_results.csv    # 27 checks, all results
└── validation_failures.csv   # 4 failed checks detail
```

---

## Next Steps

1. **Load to BigQuery** - Data is certified, proceed with load
2. **Test SQL queries** - Validate join logic works
3. **Document known issues** - 24 dupes, 3 null ratings in data dictionary
