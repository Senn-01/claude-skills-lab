---
version: 0.1.0
created: 2025-12-24
project: orange-cx-intelligence-agent
status: complete
---

# Implementation Log: Orange CX Intelligence Agent

## Overview

Customer feedback data pipeline for Orange Belgium. 5-phase data-analyst workflow completed with 99.9% quality certification.

## Painpoints & Solutions

### Painpoint 1: MOBIS Code Case Mismatch

**Problem**: id_business had `mobis467` (lowercase), SMS had `MOBIS467` (uppercase). Join only matched 30%.

**Solution**: Normalize to uppercase in cleaning script.
```python
dim_shops['mobis_code'] = dim_shops['mobis_code'].str.upper()
```
**Result**: Join improved from 30% → 64%.

---

### Painpoint 2: CSV Multiline Text Breaks BigQuery

**Problem**: Google Reviews verbatim field had embedded `\n` newlines. BigQuery CSV parser error: "too many errors, giving up".

**Solution**: Export as JSONL (JSON Lines) instead of CSV.
```python
df.to_json('table.jsonl', orient='records', lines=True)
```
**Result**: JSONL loads cleanly - newlines escaped as `\n` in JSON strings.

---

### Painpoint 3: Incomplete Shop Master

**Problem**: id_business had 161 shops, but SMS surveys referenced 28 additional MOBIS codes. 1,218 SMS records couldn't be mapped.

**Solution**: Accept partial coverage, flag with `is_mappable` boolean.
- 63.8% SMS → dim_shops (full context)
- 36.2% SMS kept with NULL shop_id (analyze by channel/MOBIS)

**Lesson**: Master data is rarely complete. Design for graceful degradation.

---

### Painpoint 4: Language Field 72% Empty

**Problem**: IAM-Language column sparse. Needed language for SQL agent prompts.

**Solution**: Infer from Belgian postal codes:
```python
def infer_language_from_zip(zipcode):
    if 1000 <= z <= 1299: return 'BI'  # Brussels bilingual
    if 4000 <= z <= 7999: return 'FR'  # Wallonia
    else: return 'NL'  # Flanders
```
**Result**: 100% language coverage.

---

### Painpoint 5: CLOSED Shops Polluting Master Data

**Problem**: full_shop_infos had 2,224 rows but 835 (37.5%) were Macro-Segment = "CLOSED" (defunct businesses).

**Solution**: Filter early in cleaning pipeline.
```python
shop_info_active = shop_info[shop_info['macro_segment'] != 'CLOSED']
```
**Lesson**: EDA reveals what "clean" means. CLOSED was a business status, not a flag error.

---

## Key Learnings

| Topic | Insight |
|-------|---------|
| **Case sensitivity** | Always normalize keys (uppercase) before joins |
| **Text fields** | Use JSONL for BigQuery when text contains newlines |
| **Master data** | Design for incomplete references (NULL FKs) |
| **Domain inference** | Belgian postal codes reliably map to language regions |
| **EDA value** | Status fields like "CLOSED" reveal business meaning, not data errors |

## Outputs

- 3 clean tables: `dim_shops` (161), `fact_google_reviews` (1,815), `fact_sms_surveys` (5,268)
- Quality certified at 99.9% (threshold 95%)
- LLM context doc ready for SQL agent injection
