---
phase: understand
project: orange-cx-intelligence
date: 2025-12-22T12:30:00Z
status: complete
stakeholders: [Astrid, Aurore, District/KAM Managers, Shop Advisors]
linked_files:
  - cases/orange-cx-intelligence-agent/docs/scratchpad-orange-feedback-agent.md
  - ai-docs/research-bigquery-csv.md
---

# Business Understanding: Orange CX Intelligence Agent

## Problem Statement

**In one sentence:**
Prepare customer feedback data from CSV exports (Google Reviews + SMS Surveys + Shop metadata) into clean BigQuery tables that an SQL agent can query conversationally.

**Full context:**
Orange Belgium operates ~100 retail shops where customers can purchase products, activate services, and get support. Customer feedback exists in two forms: Google Reviews (with AI-generated responses) and post-transaction SMS surveys. This data currently sits in spreadsheets, unanalyzed.

The business need is an AI agent that management and shop teams can query conversationally ("Top 5 complaints for shop X in November") to extract actionable insights. The agent provides **external authority** for change management—"the customer says X" carries more weight than "management says X."

This phase focuses on **data preparation for BigQuery**, not analysis. The SQL agent will do the querying; we need clean, well-structured tables.

---

## Decision Context

### The Decision
How to structure BigQuery tables to support natural language queries about customer feedback.

### The Options
1. **Denormalized single table** - Combine all feedback sources with shop info
2. **Star schema** - Fact table (feedback) + dimension tables (shops, time)
3. **Source-aligned** - Separate tables per source, join at query time

### Decision Threshold
Tables must support these query types:
- Time filtering (week, month, quarter, custom)
- Shop filtering (single, district, region, all)
- Theme extraction (verbatim text available)
- Quantification (counts with denominators)
- Ranking/comparison across shops

### Decision Maker
Dev-0 (developer building the Nexus agent)

---

## Scope

### In Scope
- Design BigQuery table schema for customer feedback data
- Clean and load 4 source CSVs
- Ensure tables support required query patterns
- Document data definitions and known issues

### Out of Scope
- Building the SQL agent (done separately on Nexus platform)
- Theme extraction logic (LLM-prompted, not in data layer)
- Report generation (PPTX/PDF - agent capability)
- Google Review response workflow (separate existing system)

### Time Period
Data appears to cover 2025 (July-November based on samples)

### Segments/Filters
- Shop types: Orange owned shops, distributors, B2B partners
- Geography: Belgium (Flemish + Francophone regions)
- Channels: OSO (Orange Shops), TZ Carrefour, Indirect

---

## Success Criteria

### What "Done" Looks Like
- All 4 CSV files loaded into BigQuery
- Tables support the example queries from requirements
- Data quality issues documented and handled
- Schema documented for SQL agent reference

### Acceptance Criteria
- [ ] Google Reviews table with: timestamp, rating, verbatim, shop_id, AI response
- [ ] SMS Survey table with: timestamp, score, verbatim, shop_id, case type
- [ ] Shops dimension table with: shop_id, name, city, manager, KAM
- [ ] Joins work correctly across tables
- [ ] Date/time fields properly typed for filtering

### Validation Approach
Test queries that match the example requirements:
- "Top 5 complaints for shop X in November"
- "How did shop Y perform last month?"
- "What improvements should we prioritize by volume?"

---

## Data Landscape

### Source Tables

| Source | File | Records (est.) | Purpose |
|--------|------|----------------|---------|
| Google Reviews | `google-review-ai-answers.csv` | ~100s | Customer reviews + AI responses |
| SMS Surveys | `sms-client-feedback.csv` | ~1000s | Post-transaction satisfaction |
| Shop Master | `id-business.csv` | ~100 | Shop ID → name/location |
| Full Shop Info | `full-shop-infos.csv` | ~200+ | Management hierarchy, segments |

### Field Inventory

#### google-review-ai-answers.csv
| Field | Type | Description | Notes |
|-------|------|-------------|-------|
| Business_ID | STRING | MongoDB ObjectId | Join key to shops |
| Review_ID | STRING | Google Review ID | Unique identifier |
| Timestamp_Client_Feedback | TIMESTAMP | When review was posted | ISO 8601 format |
| Client_Feedback | STRING | Review text (translated) | May be null |
| Client_Rating | INT | 1-5 star rating | Required |
| Client_Name | STRING | Reviewer name | PII consideration |
| Timestamp_Ai_Agent_Response | TIMESTAMP | When AI responded | May differ from review |
| Ai_Agent_Response | STRING | Generated response | Multilingual (FR/NL) |
| Shop_Name | STRING | Denormalized shop name | Redundant |
| Key_Account_Manager_Email | STRING | KAM email | Sparse |
| Shop_Manager | STRING | Manager name | Sparse |
| Correction | STRING | Manual correction to AI response | Business flag |
| Duplicates | STRING | Duplicate flag | Data quality |
| TimeStamp | STRING | Processing timestamp | May be redundant |

#### sms-client-feedback.csv
| Field | Type | Description | Notes |
|-------|------|-------------|-------|
| Response Date | DATE | When survey was completed | DD/MM/YYYY format |
| Interaction date | DATE | When transaction occurred | DD/MM/YYYY format |
| SHOP_Shop Name + Aramis code | STRING | Shop name + MOBIS code | Parse required |
| SHOP_Vendor | STRING | Vendor ID | Staff tracking |
| Satisfaction score | INT | 1-5 rating | Required |
| Verbatim | STRING | Free-text comment | Often empty |
| Respondent ID | STRING | Survey respondent ID | Unique |
| SHOP_Shop AudienceName | STRING | SUBSCRIPTION/Prospect | Customer type |
| SHOP_City | STRING | Shop city (with prefix) | "B- 1082" format |
| SHOP_Customer Type | STRING | SUBSCRIBERS/FIRMS/N/A | Segment |
| SHOP_Channel | STRING | OSO/TZ Carrefour | Distribution channel |
| SHOP_Direction | STRING | Orange shops/Indirect | High-level channel |
| SHOP_Mainchain | STRING | MOBISTAR OWNED SHOPS, etc. | Ownership |
| SHOP_Case type | STRING | New Activation/ACCESSORY/etc. | Transaction type |
| SHOP_Case level 1-3 | STRING | Hierarchical case categorization | Often N/A |
| SHOP_Source file | STRING | Activation/Purchase | Source system |

#### id-business.csv
| Field | Type | Description | Notes |
|-------|------|-------------|-------|
| id | STRING | MongoDB ObjectId | Primary key |
| name | STRING | Shop name | |
| code | STRING | MOBIS code | Join key |
| city | STRING | City name | |
| address | STRING | Street address | |
| zipcode | STRING | Postal code | |
| full name | STRING | Name + City | Redundant |

#### full-shop-infos.csv
| Field | Type | Description | Notes |
|-------|------|-------------|-------|
| Macro-Segment | STRING | Shop classification | Distributor, Retail, B2B |
| Type of own shop | STRING | Shop type detail | Often empty |
| new mainchain | STRING | Chain/partner name | BPOST, EXELLENT, etc. |
| Aramis code | STRING | MOBIS code | Join key |
| External Partner code | STRING | Partner ID | Often NA |
| POS name | STRING | Point of sale name | |
| Address, Box, Zip, City | STRING | Location fields | |
| Shop manager name | STRING | Manager name | |
| Shop Manager email | STRING | Manager email | |
| District / Key account manager name | STRING | KAM name | |
| District / Key account manager email | STRING | KAM email | |
| AREA | STRING | Geographic area | Often empty |
| Regional Sales manager name/email | STRING | RSM details | |
| TSS manager | STRING | TSS manager | |
| IAM - Language | STRING | NL/FR | Language region |

### Key Definitions

| Term | Business Definition | Data Representation |
|------|---------------------|---------------------|
| MOBIS code | Orange internal shop identifier | "MOBIS" + 3 digits (e.g., MOBIS519) |
| Aramis code | Same as MOBIS code | Used interchangeably in different systems |
| Verbatim | Free-text customer comment | STRING field, often empty in SMS |
| KAM | Key Account Manager - regional manager | Email in multiple tables |
| Macro-Segment | Shop classification | Distributor, Retail Others, B2B Indirect, Orange Shops |
| OSO | Orange Shop Owned | Channel type for owned shops |

### Known Data Limitations

- **Date format inconsistency**: SMS uses DD/MM/YYYY, Google Reviews uses ISO 8601
- **Shop ID join complexity**: Google Reviews uses MongoDB ObjectId, SMS uses MOBIS code embedded in shop name string
- **Sparse verbatims**: Many SMS surveys have empty Verbatim fields
- **Multilingual content**: Reviews in French, Dutch, and sometimes translated
- **PII present**: Customer names in reviews, manager emails in shop data
- **Duplicate flagging**: Some records marked as duplicates in Google Reviews

---

## Header Quality Assessment

### Current State

| File | Quality | Issues |
|------|---------|--------|
| `google-review-ai-answers` | Mixed | Mixed case, trailing empty cols, inconsistent (Ai vs AI) |
| `sms-client-feedback` | Poor | Spaces, parentheses, SHOP_ prefix, plus signs |
| `id-business` | Good | Minor: "full name" has space |
| `full-shop-infos` | Poor | Spaces, slashes, verbose, inconsistent |

### Worst Offenders

```
SMS:  "Satisfaction score (score on scale from 1 to 5)"  ← Parentheses, spaces, redundant
SMS:  "SHOP_Shop Name + Aramis code"                     ← Prefix, plus sign, compound value
Shop: "District / Key account manager name"              ← Slashes, spaces
Shop: "Shop Manager/ private shop email"                 ← Inconsistent slash spacing
```

### BigQuery Column Naming Best Practices

| Rule | Example | Why |
|------|---------|-----|
| **snake_case** | `client_rating` not `Client_Rating` | BigQuery convention, case-insensitive |
| **No spaces** | `response_date` not `Response Date` | Avoids quoting in SQL |
| **No special chars** | `shop_name` not `Shop Name + Code` | Prevents syntax errors |
| **No prefixes** | `vendor_id` not `SHOP_Vendor` | Prefix belongs to table name, not column |
| **Lowercase** | `timestamp` not `TimeStamp` | Consistency |
| **Singular nouns** | `case_type` not `case_types` | Unless truly plural |
| **Descriptive but concise** | `kam_email` not `District / Key account manager email` | Readable SQL |

### Column Mapping: google-review-ai-answers → `fact_google_reviews`

| Original | Target | Action |
|----------|--------|--------|
| Business_ID | `shop_id` | Rename (FK to dim_shops) |
| Review_ID | `review_id` | Rename (PK) |
| Timestamp_Client_Feedback | `review_timestamp` | Rename |
| Client_Feedback | `verbatim` | Rename (consistent with SMS) |
| Client_Rating | `rating` | Rename |
| Client_Name | `client_name` | Keep (PII flag) |
| Timestamp_Ai_Agent_Response | `response_timestamp` | Rename |
| Ai_Agent_Response | `ai_response` | Rename |
| Shop_Name | — | DROP (redundant, in dim) |
| Key_Account_Manager_Email | — | DROP (redundant, in dim) |
| Shop_Manager | — | DROP (redundant, in dim) |
| Correction | `correction_text` | Rename |
| Duplicates | `is_duplicate` | Rename → Boolean |
| TimeStamp,,, | — | DROP (empty/redundant) |

### Column Mapping: sms-client-feedback → `fact_sms_surveys`

| Original | Target | Action |
|----------|--------|--------|
| Response Date | `response_date` | Rename |
| Interaction date | `interaction_date` | Rename |
| SHOP_Shop Name + Aramis code | `shop_id` | Extract MOBIS code, FK to dim |
| SHOP_Vendor | `vendor_id` | Rename |
| Satisfaction score (...) | `rating` | Rename (consistent with Google) |
| Verbatim | `verbatim` | Keep |
| Respondent ID | `survey_id` | Rename (PK) |
| SHOP_Shop AudienceName | `audience_type` | Rename |
| SHOP_City | — | DROP (in dim_shops) |
| SHOP_Customer Type | `customer_type` | Rename |
| SHOP_Channel | `channel` | Rename |
| SHOP_Direction | — | DROP (derivable) |
| SHOP_Mainchain | — | DROP (in dim_shops) |
| SHOP_Case type | `case_type` | Rename |
| SHOP_Case level 1-3 | `case_category` | Flatten or hierarchy |
| SHOP_Source file | `source_system` | Rename |

### Column Mapping: dim_shops (merged)

| Target | Source | Notes |
|--------|--------|-------|
| `shop_id` | id-business.id | PK (MongoDB ObjectId) |
| `mobis_code` | id-business.code | MOBIS### format |
| `name` | id-business.name | Shop name |
| `city` | id-business.city | |
| `address` | id-business.address | |
| `zipcode` | id-business.zipcode | |
| `macro_segment` | full-shop-infos.Macro-Segment | |
| `mainchain` | full-shop-infos.new mainchain | |
| `shop_manager_name` | full-shop-infos.Shop manager name | |
| `shop_manager_email` | full-shop-infos.Shop Manager email | |
| `kam_name` | full-shop-infos.District / Key account manager name | |
| `kam_email` | full-shop-infos.District / Key account manager email | |
| `rsm_name` | full-shop-infos.Regional Sales manager name | |
| `rsm_email` | full-shop-infos.Regional Sales manager email | |
| `language` | full-shop-infos.IAM - Language | NL/FR |

### Recommendation

**Rename on load, not in source files.** Preserve source integrity while giving BigQuery clean column names.

```python
# Example: pandas rename on load
column_mapping = {
    "Satisfaction score (score on scale from 1 to 5)": "rating",
    "SHOP_Shop Name + Aramis code": "shop_name_code",  # Then extract MOBIS
    "Response Date": "response_date",
    "Interaction date": "interaction_date",
    # ...
}
df = pd.read_csv("sms-client-feedback.csv").rename(columns=column_mapping)
```

---

## Proposed BigQuery Schema

### Option: Star Schema (Recommended)

```
                    ┌─────────────────┐
                    │   dim_shops     │
                    │─────────────────│
                    │ shop_id (PK)    │
                    │ mobis_code      │
                    │ name            │
                    │ city            │
                    │ region          │
                    │ language        │
                    │ macro_segment   │
                    │ kam_name        │
                    │ kam_email       │
                    │ rsm_name        │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ fact_google_  │    │ fact_sms_     │    │ dim_time      │
│ reviews       │    │ surveys       │    │ (optional)    │
│───────────────│    │───────────────│    │───────────────│
│ review_id(PK) │    │ survey_id(PK) │    │ date_key      │
│ shop_id (FK)  │    │ shop_id (FK)  │    │ year          │
│ timestamp     │    │ interaction_  │    │ quarter       │
│ rating        │    │   date        │    │ month         │
│ verbatim      │    │ response_date │    │ week          │
│ ai_response   │    │ score         │    └───────────────┘
│ corrected     │    │ verbatim      │
│ client_name   │    │ vendor_id     │
└───────────────┘    │ case_type     │
                     │ customer_type │
                     └───────────────┘
```

### Field Transformations Required

| Source Field | Target Field | Transformation |
|--------------|--------------|----------------|
| SMS: `SHOP_Shop Name + Aramis code` | `shop_id` | Extract MOBIS code with regex |
| SMS: `Interaction date` | `interaction_date` | Parse DD/MM/YYYY → DATE |
| SMS: `SHOP_City` | `city` | Remove "B- " prefix |
| Google: `Business_ID` | `shop_id` | Map via id-business lookup |
| Google: `Timestamp_Client_Feedback` | `timestamp` | Parse ISO 8601 → TIMESTAMP |
| Google: `Correction` | `is_corrected` | Boolean (non-empty = true) |

---

## Assumptions

**We are assuming that:**

1. **MOBIS codes are stable identifiers** — *Impact if wrong: joins will fail*
2. **Timestamps are in consistent timezone** — *Impact if wrong: time filtering errors*
3. **All shops in feedback exist in master data** — *Impact if wrong: orphan records*
4. **Verbatim language matches shop region** — *Impact if wrong: theme extraction complexity*

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Shop ID mapping failures | Medium | High | Build lookup table, log unmapped records |
| Date parsing errors | Medium | Medium | Use BigQuery's SAFE_PARSE functions |
| Large verbatim text size | Low | Low | BigQuery handles large strings |
| Schema evolution | Medium | Medium | Use NULLABLE fields, version schema |

---

## Implementation Approach: Clean Google Sheets (Scenario 2)

### Decision

Rather than maintaining messy source headers with a transformation layer, we propose **restructuring the client's Google Sheets** into a clean 3-tab format that maps directly to BigQuery.

### Why This Approach

| Aspect | Keep Messy Headers | Clean Sheets (Chosen) |
|--------|--------------------|-----------------------|
| Transformation layer | Required (ongoing maintenance) | None |
| BigQuery connection | Complex (raw → transform → semantic) | Direct |
| Future data | Same problems repeat | Clean from start |
| Debugging | "Which layer broke?" | Single source of truth |
| Client learning | No improvement | Better data practices |

### Target Google Sheet Structure

**3 sheets instead of 4** (merge id-business + full-shop-infos):

#### Sheet 1: `shops`
```
shop_id | mobis_code | name | city | address | zipcode | macro_segment | mainchain | shop_manager_name | shop_manager_email | kam_name | kam_email | rsm_name | rsm_email | language
```

#### Sheet 2: `google_reviews`
```
review_id | shop_id | review_timestamp | rating | verbatim | client_name | response_timestamp | ai_response | correction_text | is_duplicate
```

#### Sheet 3: `sms_surveys`
```
survey_id | shop_id | interaction_date | response_date | rating | verbatim | vendor_id | audience_type | customer_type | channel | case_type | case_category | source_system
```

### Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              CLIENT'S CLEAN GOOGLE SHEETS                        │
│     shops | google_reviews | sms_surveys                         │
│     (clean headers, validated, single source of truth)           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
              [BigQuery Connected Sheets OR Scheduled Export]
              (zero transformation - direct mapping)
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       BIGQUERY                                   │
│       dim_shops | fact_google_reviews | fact_sms_surveys         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    [SQL Agent on Nexus]
```

### Implementation Phases

| Phase | Description | Output |
|-------|-------------|--------|
| 1. Explore | Profile current data quality | EDA report with issues |
| 2. Design | Finalize schema based on EDA | Clean sheet template |
| 3. Migrate | Transform + load existing data | Populated clean sheet |
| 4. Validate | Verify data integrity | Validation report |
| 5. Connect | Link BigQuery to clean sheet | Working pipeline |
| 6. Handoff | Document + train client | Data dictionary |

### Deliverables

1. **Template Google Sheet** - `orange-cx-feedback-v2`
   - 3 tabs with clean headers
   - Data validation on key fields (dropdowns, formats)
   - Protected header row

2. **Migration Script** - `migrate_to_clean_structure.py`
   - Reads 4 source CSVs
   - Merges shop data
   - Maps shop IDs across sources
   - Outputs 3 clean CSVs (importable to Sheets)

3. **Validation Report** - Row counts, orphans, quality issues

4. **Data Dictionary** - Field definitions, allowed values, business rules

---

## Next Steps

1. [x] Document business understanding (this document)
2. [x] Decide on implementation approach (Scenario 2: Clean Sheets)
3. [ ] Run `/data-explore` to profile data quality
4. [ ] Design final schema based on EDA findings
5. [ ] Create migration script
6. [ ] Generate clean Google Sheet with migrated data
7. [ ] Connect BigQuery and validate with test queries

---

## Reference Documents

- `cases/orange-cx-intelligence-agent/docs/scratchpad-orange-feedback-agent.md` - Full project context
- `ai-docs/research-bigquery-csv.md` - BigQuery CSV loading best practices
