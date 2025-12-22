---
phase: explore
project: orange-cx-intelligence
date: 2025-12-22T09:01:00Z
status: complete
prior_phase: ai-docs/data-understand-orange-cx-intelligence.md
linked_files:
  - cases/orange-cx-intelligence-agent/eda_orange_cx.py
  - cases/orange-cx-intelligence-agent/eda_output/
---

# EDA Report: Orange CX Intelligence

## Why EDA?

> "EDA is detective work, not random poking."

We explored 4 source datasets BEFORE cleaning to understand:
- What the data actually looks like (vs. what we expected)
- What quality issues exist and their severity
- How to correctly join across datasets
- What cleaning decisions to make

---

## Dataset Overview

| Dataset | Rows | Columns | Complete % | Purpose |
|---------|------|---------|------------|---------|
| google_reviews | 1,829 | 17 | 0% | Customer reviews + AI responses |
| sms_surveys | 5,268 | 18 | 6% | Post-transaction satisfaction |
| id_business | 161 | 7 | 100% | Shop ID → name/location |
| full_shop_infos | 2,224 | 19 | 0% | Management hierarchy |

**Key Findings:**
- Google Reviews: 0% complete rows due to many sparse/empty columns (KAM email, Shop Manager, trailing empty columns)
- SMS Surveys: 77.9% verbatims are empty (only 22.1% have free-text comments)
- id_business: Cleanest dataset, fully complete
- full_shop_infos: 2,224 rows but includes 835 CLOSED shops (37.5%)

---

## Date Range Analysis

| Dataset | Field | Range |
|---------|-------|-------|
| google_reviews | Timestamp_Client_Feedback | July 2025 - November 2025 |
| google_reviews | TimeStamp (processing) | Oct 20, 2025 - Dec 18, 2025 |
| sms_surveys | Response Date | Nov 1-30, 2025 |
| sms_surveys | Interaction date | Aug 25 - Nov 27, 2025 |

**Key Findings:**
- SMS surveys cover November 2025 only
- Google Reviews span July-November 2025
- 99.1% of Google timestamps are parseable

---

## Rating Distribution

### Google Reviews (Client_Rating)

Values are 1-5 stars. Distribution not fully analyzed, but sample shows both 1-star and 5-star ratings present.

### SMS Surveys (Satisfaction score)

| Metric | Value |
|--------|-------|
| Count | 5,268 |
| Mean | 4.64 |
| Median | 5.00 |
| Std | 0.81 |
| Min | 1 |
| Max | 5 |

**Key Finding:** Highly positive skew. Most customers rate 5 stars. Q1=5, Q3=5 indicates majority are 5s. This is common for satisfaction surveys (response bias toward satisfied customers).

---

## Shop ID Join Analysis

**WHY**: We need to join feedback to shops. Each dataset uses different identifiers.

### Identifier Overview

| Dataset | ID Field | Unique Values | Format | Example |
|---------|----------|---------------|--------|---------|
| id_business | id | 161 | MongoDB ObjectId | `6669610334fb243c680a7680` |
| id_business | code | 161 | MOBIS code | `MOBIS499` |
| google_reviews | Business_ID | 145 | MongoDB ObjectId | `668c003316119aced8009790` |
| sms_surveys | Shop Name + Aramis code | embedded | Text + MOBIS | `ORANGE SHOP WATERLOO - MOBIS344` |
| full_shop_infos | Aramis code | 2,211 | Various codes | `BPOST002`, `MOBIS519` |

### Join Strategy

```
                    id_business.id
                         ↓
              google_reviews.Business_ID
              (MongoDB ObjectId join)

                    id_business.code
                         ↓
              sms_surveys → extract MOBIS from "Shop Name + Aramis code"
              (MOBIS code extraction: 87% success rate)
```

**Key Findings:**
- Google Reviews: 145 unique Business_IDs vs 161 shops in master = 16 shops have no reviews
- SMS Surveys: MOBIS extraction succeeds for 4,581/5,268 records (87%)
- full_shop_infos: 2,211 Aramis codes but includes non-MOBIS codes (BPOST, etc.)
- 687 SMS records (13%) cannot be joined via MOBIS extraction

---

## Missing Value Analysis

### google_reviews (17 columns)

| Column | Missing % | Action |
|--------|-----------|--------|
| Key_Account_Manager_Email | 100% | DROP - empty |
| Shop_Manager | 100% | DROP - empty |
| Unnamed: 14 | 100% | DROP - artifact |
| Unnamed: 15 | 100% | DROP - artifact |
| Correction | 99.95% | KEEP - business flag |
| Unnamed: 16 | 99.95% | DROP - sparse artifact |
| Timestamp_Ai_Agent_Response | 48.1% | KEEP - valid for responded reviews |
| Review_ID | 0.8% | INVESTIGATE - should be 0% |

**Column Cleanup:** Remove 5 empty/artifact columns. Keep core fields.

### sms_surveys (18 columns)

| Column | Missing % | Action |
|--------|-----------|--------|
| Verbatim | 77.9% | KEEP - expected sparsity |
| SHOP_Case level 1 | 68.3% | KEEP - optional hierarchy |
| SHOP_Case level 2 | 68.3% | KEEP - optional hierarchy |
| SHOP_Case level 3 | 68.3% | KEEP - optional hierarchy |
| All other columns | <1% | KEEP |

**Key Finding:** Verbatim sparsity is expected - many customers rate but don't comment. Case levels are optional categorization.

### full_shop_infos (19 columns)

| Column | Missing % | Reason |
|--------|-----------|--------|
| Type of own shop | 95.7% | Only applies to Orange-owned shops |
| External Partner code | 96.4% | Only applies to partners |
| Box | 67.1% | Address sub-field |
| Shop manager name | 84.8% | Sparse management data |
| Shop Manager email | 86.2% | Sparse |
| AREA | 94.8% | Sparse |
| TSS manager | 86.7% | Sparse |
| IAM - Language | 71.9% | NL/FR language tag |

**Key Finding:** High missingness is by design - not all fields apply to all shop types. Orange-owned shops have more complete data than distributors.

---

## Categorical Analysis

### full_shop_infos.Macro-Segment

| Segment | Count | % |
|---------|-------|---|
| DISTRIBUTORS | 898 | 40.4% |
| CLOSED | 835 | 37.5% |
| Retail Others | 163 | 7.3% |
| Orange Shops | 97 | 4.4% |
| Distributor | 72 | 3.2% |
| Retail Carrefour | 41 | 1.8% |
| Traffic Zone - Carrefour | 40 | 1.8% |

**Key Finding:** 37.5% of shop records are CLOSED. These should be filtered for active analysis.

### sms_surveys.SHOP_Channel

| Channel | Count | % |
|---------|-------|---|
| OSO | 4,312 | 81.9% |
| TZ Carrefour | 956 | 18.1% |

**Key Finding:** Orange Shop Owned (OSO) dominates the SMS survey data.

---

## Data Quality Issues Summary

### Critical Issues

| Issue | Dataset | Records | Remediation |
|-------|---------|---------|-------------|
| Empty columns | google_reviews | 5 columns | DROP columns |
| MOBIS extraction fails | sms_surveys | 687 (13%) | Manual mapping or log as unmappable |
| Shop master mismatch | google_reviews | 16 shops | Verify Business_ID → id mapping |

### Major Issues

| Issue | Dataset | Records | Remediation |
|-------|---------|---------|-------------|
| Sparse verbatims | sms_surveys | 4,102 (78%) | Expected - not an error |
| Case level hierarchy | sms_surveys | 3,600 (68%) | Optional fields - keep nulls |
| CLOSED shops in master | full_shop_infos | 835 (37.5%) | Filter on Macro-Segment != 'CLOSED' |

### Minor Issues

| Issue | Dataset | Records | Remediation |
|-------|---------|---------|-------------|
| Trailing empty columns | google_reviews | 3 columns | DROP |
| Date format DD/MM/YYYY | sms_surveys | all | Parse with dayfirst=True |
| ISO 8601 timestamps | google_reviews | all | Standard format, direct parse |

---

## Questions for Stakeholders

1. **Shop master scope**: Should we include all 2,224 shops from full_shop_infos, or filter to the 161 in id_business?
2. **CLOSED shops**: Should closed shops be excluded entirely, or kept for historical context?
3. **SMS unmappable records**: 687 SMS surveys (13%) can't be joined to shops. Keep or drop?
4. **Review_ID missing**: 14 reviews lack Review_ID. Are these valid records?
5. **Language field sparsity**: 72% of shops lack IAM-Language. Use city/region as fallback?

---

## Recommended Cleaning Steps

### Phase 1: Column Cleanup

1. **google_reviews**: Drop 5 empty/artifact columns
   - Key_Account_Manager_Email, Shop_Manager, Unnamed: 14/15/16

2. **Rename columns** per BigQuery conventions (snake_case, no spaces)

### Phase 2: Date Parsing

3. **google_reviews**: Parse ISO 8601 timestamps → TIMESTAMP
4. **sms_surveys**: Parse DD/MM/YYYY → DATE with dayfirst=True

### Phase 3: ID Normalization

5. **sms_surveys**: Extract MOBIS code from "SHOP_Shop Name + Aramis code"
   - Pattern: `(MOBIS\d+)`
   - Handle 687 unextractable records

6. **Create shop_id mapping table**:
   - id_business.id ↔ id_business.code (MOBIS)
   - Join google_reviews.Business_ID → id
   - Join sms_surveys.extracted_mobis → code

### Phase 4: Master Data Merge

7. **Merge shop data**: id_business + filtered full_shop_infos
   - Filter: Macro-Segment != 'CLOSED'
   - Join on Aramis code (MOBIS)
   - Prefer id_business values for conflicts

### Phase 5: Validation

8. **Verify join completeness**:
   - All google_reviews have matching shop
   - All sms_surveys (with MOBIS) have matching shop
   - Log orphan records

---

## Exit Criteria Status

| Criterion | Status |
|-----------|--------|
| Understand structure of every column | Done |
| Quantified all data quality issues | Done |
| Prioritized list of cleaning tasks | Done |
| Validated data against business definitions | Partial - need stakeholder input |
| Documented findings | Done |
| Stakeholders reviewed critical findings | Pending |

**Ready to proceed to Data Cleaning** after stakeholder clarification on 5 questions above.

---

## Artifacts

- EDA Script: `cases/orange-cx-intelligence-agent/eda_orange_cx.py`
- Column Summaries: `cases/orange-cx-intelligence-agent/eda_output/*_columns.csv`
- Quality Issues: `cases/orange-cx-intelligence-agent/eda_output/quality_issues.csv`
