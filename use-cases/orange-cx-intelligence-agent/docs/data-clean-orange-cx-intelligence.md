---
phase: clean
project: orange-cx-intelligence
date: 2025-12-22T09:12:00Z
status: complete
prior_phase: ai-docs/data-explore-orange-cx-intelligence.md
linked_files:
  - cases/orange-cx-intelligence-agent/clean_orange_cx.py
  - cases/orange-cx-intelligence-agent/clean_output/
---

# Data Cleaning Report: Orange CX Intelligence

## Summary

Transformed 4 raw CSV files into 3 clean, BigQuery-ready tables:

| Table | Rows | Columns | Purpose |
|-------|------|---------|---------|
| `dim_shops` | 161 | 15 | Shop dimension (active shops) |
| `fact_google_reviews` | 1,815 | 11 | Google Reviews fact table |
| `fact_sms_surveys` | 5,268 | 17 | SMS Survey fact table |

---

## Decisions Applied

| Decision | Action | Rationale |
|----------|--------|-----------|
| CLOSED shops | Filtered out | 835 defunct businesses, no feedback data links to them |
| Empty columns | Dropped 5 | Key_Account_Manager_Email, Shop_Manager, Unnamed_14/15/16 - all 100% null |
| Missing Review_ID | Dropped 14 rows | 0.8% of records, incomplete data |
| MOBIS case mismatch | Normalized to uppercase | id_business had mixed case (`mobis467`), SMS had uppercase (`MOBIS467`) |
| Language sparsity | Inferred from zip code | Belgian postal codes map to language regions |
| Unmappable SMS | Kept with NULL shop_id | 1,905 records from Carrefour/SMART + shops not in id_business |

---

## Pipeline Steps

### 1. dim_shops

**Source**: id_business (161 rows) + full_shop_infos (2,224 rows)

| Step | Operation | Before | After | Change |
|------|-----------|--------|-------|--------|
| 1 | Filter CLOSED from full_shop_infos | 2,224 | 1,389 | -835 |
| 2 | Normalize MOBIS codes (uppercase) | - | - | Format fix |
| 3 | LEFT JOIN enrichment | 161 | 161 | +0 |
| 4 | Infer language from zipcode | 53 missing | 0 missing | 100% coverage |

**Final Schema**:
```
shop_id          STRING   MongoDB ObjectId (PK)
mobis_code       STRING   MOBIS### format
shop_name        STRING   Shop name
city             STRING   City
address          STRING   Street address
zipcode          STRING   Postal code
macro_segment    STRING   Distributor/Retail/Orange Shops
new_mainchain    STRING   Chain/partner name
manager_name     STRING   Shop manager
manager_email    STRING   Manager email
kam_name         STRING   Key Account Manager
kam_email        STRING   KAM email
rsm_name         STRING   Regional Sales Manager
rsm_email        STRING   RSM email
language         STRING   NL/FR/BI (inferred from zip)
```

---

### 2. fact_google_reviews

**Source**: google-review-ai-answers.csv (1,829 rows)

| Step | Operation | Before | After | Change |
|------|-----------|--------|-------|--------|
| 1 | Clean column names | - | - | Standardized |
| 2 | Drop empty/unnamed columns | 17 cols | 12 cols | -5 |
| 3 | Drop missing review_id | 1,829 | 1,815 | -14 |
| 4 | Parse ISO 8601 timestamps | - | - | Datetime type |
| 5 | Create is_corrected boolean | - | - | From correction_text |

**Final Schema**:
```
review_id            STRING     Google Review ID (PK)
shop_id              STRING     FK to dim_shops
review_timestamp     TIMESTAMP  When review was posted
rating               INT64      1-5 stars
verbatim             STRING     Review text (translated)
client_name          STRING     Reviewer name
response_timestamp   TIMESTAMP  When AI responded
ai_response          STRING     Generated response
is_corrected         BOOLEAN    True if manually corrected
correction_text      STRING     Manual correction (if any)
duplicate_flag       STRING     'ok' flag from source
```

**Join Validation**: 1,815/1,815 (100%) link to dim_shops ✓

---

### 3. fact_sms_surveys

**Source**: sms-client-feedback.csv (5,268 rows)

| Step | Operation | Before | After | Change |
|------|-----------|--------|-------|--------|
| 1 | Clean column names | - | - | Removed SHOP_ prefix |
| 2 | Extract MOBIS from shop name | 5,268 | 4,581 extracted | 87% success |
| 3 | Map MOBIS to shop_id | 4,581 | 3,363 mapped | 63.8% coverage |
| 4 | Parse DD/MM/YYYY dates | - | - | Date type |
| 5 | Flag unmappable records | - | - | is_mappable column |

**Final Schema**:
```
survey_id          STRING   Respondent ID (PK)
shop_id            STRING   FK to dim_shops (nullable)
mobis_code         STRING   Extracted MOBIS### (nullable)
interaction_date   DATE     When transaction occurred
response_date      DATE     When survey completed
rating             INT64    1-5 satisfaction
verbatim           STRING   Free-text comment (78% null)
vendor_id          STRING   Staff ID
audience_type      STRING   SUBSCRIPTION/Prospect
customer_type      STRING   SUBSCRIBERS/FIRMS/N/A
channel            STRING   OSO/TZ Carrefour/SMART/etc
case_type          STRING   New Activation/ACCESSORY/etc
case_level_1       STRING   Hierarchical category (optional)
case_level_2       STRING   Hierarchical category (optional)
case_level_3       STRING   Hierarchical category (optional)
source_system      STRING   Activation/Purchase
is_mappable        BOOLEAN  True if shop_id linked
```

**Join Breakdown**:

| Category | Records | % | Notes |
|----------|---------|---|-------|
| Mapped to dim_shops | 3,363 | 63.8% | Full shop context available |
| MOBIS not in id_business | 1,218 | 23.1% | Shop list incomplete (28 MOBIS codes) |
| Non-MOBIS channels | 687 | 13.0% | TZ Carrefour (456), SMART (110), etc |

---

## Join Diagram

```
                    dim_shops
                    ─────────
                    shop_id (PK)
                    mobis_code
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
  fact_google_      fact_sms_        (unmapped SMS)
    reviews          surveys
  ─────────────    ─────────────    ─────────────────
  shop_id (FK)     shop_id (FK)     mobis_code only
  100% linked      63.8% linked     36.2% partial
```

---

## Data Quality After Cleaning

| Metric | Value |
|--------|-------|
| dim_shops complete rows | 100% (all have shop_id, mobis_code) |
| dim_shops with language | 100% (inferred from zip) |
| fact_google_reviews complete | 100% (review_id, shop_id, rating) |
| fact_sms_surveys with rating | 100% |
| fact_sms_surveys with verbatim | 22.1% (expected sparsity) |

---

## Known Limitations

1. **id_business incomplete**: 28 MOBIS codes in SMS surveys aren't in id_business. These shops can be analyzed by MOBIS code but not linked to dimension table.

2. **TZ Carrefour/SMART different ID system**: 687 SMS records use MCOAT/CONSU codes instead of MOBIS. Would need separate mapping table for full coverage.

3. **shop_id is MongoDB ObjectId**: Google Reviews use this ID. If source system changes, ID format may change.

4. **Timestamps are UTC**: Google Review timestamps converted to UTC. May need timezone handling for Belgian local time.

---

## Output Files

```
cases/orange-cx-intelligence-agent/clean_output/
├── dim_shops.csv              # 161 rows × 15 columns
├── fact_google_reviews.csv    # 1,815 rows × 11 columns
├── fact_sms_surveys.csv       # 5,268 rows × 17 columns
└── cleaning_log.csv           # 7 operations logged
```

---

## Next Steps

1. **Run `/data-validate`** - Certify data quality before BigQuery load
2. **Create BigQuery tables** - Define schema and load CSVs
3. **Test SQL queries** - Verify join logic with sample queries:
   - "Top 5 complaints for shop X in November"
   - "Average rating by channel"
   - "Shops with most negative feedback"
