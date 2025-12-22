#!/usr/bin/env python3
"""
Data Cleaning Script: Orange CX Intelligence
=============================================
Transforms 4 raw CSV files into 3 clean BigQuery-ready tables:
- dim_shops: Shop dimension table (merged from id_business + full_shop_infos)
- fact_google_reviews: Google Reviews fact table
- fact_sms_surveys: SMS Survey fact table

Decisions applied (from EDA analysis):
- CLOSED shops filtered out (defunct businesses)
- 687 unmappable SMS records kept with NULL shop_id
- Language inferred from zip code for missing values
- 14 missing Review_ID records dropped
- Empty columns removed from google_reviews

Usage:
    uv run python clean_orange_cx.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import re

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_PATH = Path(__file__).parent / 'DB'
OUTPUT_PATH = Path(__file__).parent / 'clean_output'
OUTPUT_PATH.mkdir(exist_ok=True)

FILES = {
    'google_reviews': 'orange-cx-intelligence-db - google-review-ai-answers.csv',
    'sms_surveys': 'orange-cx-intelligence-db - sms-client-feedback.csv',
    'id_business': 'orange-cx-intelligence-db - id-business.csv',
    'full_shop_infos': 'orange-cx-intelligence-db - full-shop-infos.csv'
}

# =============================================================================
# CLEANING LOG
# =============================================================================

class CleaningLog:
    """Track all cleaning operations with before/after counts."""

    def __init__(self):
        self.operations = []

    def log(self, table: str, operation: str, description: str,
            rows_before: int, rows_after: int, cols_before: int = None, cols_after: int = None):
        entry = {
            'table': table,
            'operation': operation,
            'description': description,
            'rows_before': rows_before,
            'rows_after': rows_after,
            'rows_diff': rows_after - rows_before,
            'cols_before': cols_before,
            'cols_after': cols_after
        }
        self.operations.append(entry)
        diff = rows_after - rows_before
        sign = '+' if diff >= 0 else ''
        print(f"  [{operation}] {description}: {rows_before:,} → {rows_after:,} ({sign}{diff:,})")

    def to_dataframe(self):
        return pd.DataFrame(self.operations)


log = CleaningLog()

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def print_section(title: str):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to snake_case."""
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(r'[^a-z0-9_]', '_', regex=True)
        .str.replace(r'_+', '_', regex=True)
        .str.strip('_')
    )
    return df


def infer_language_from_zip(zipcode) -> str:
    """
    Infer language from Belgian postal code.
    - 1000-1299: Brussels (bilingual) → 'BI'
    - 1300-1499: Walloon Brabant → 'FR'
    - 1500-1999: Flemish Brabant → 'NL'
    - 2000-3999: Antwerp, Limburg → 'NL'
    - 4000-7999: Wallonia → 'FR'
    - 8000-9999: West/East Flanders → 'NL'
    """
    try:
        z = int(zipcode)
        if 1000 <= z <= 1299:
            return 'BI'  # Bilingual Brussels
        elif 1300 <= z <= 1499:
            return 'FR'
        elif 1500 <= z <= 1999:
            return 'NL'
        elif 2000 <= z <= 3999:
            return 'NL'
        elif 4000 <= z <= 7999:
            return 'FR'
        elif 8000 <= z <= 9999:
            return 'NL'
    except (ValueError, TypeError):
        pass
    return None


def extract_mobis_code(shop_name_code: str) -> str:
    """Extract MOBIS code from 'Shop Name + Aramis code' field."""
    if pd.isna(shop_name_code):
        return None
    match = re.search(r'(MOBIS\d+)', str(shop_name_code))
    return match.group(1) if match else None


# =============================================================================
# TABLE 1: dim_shops
# =============================================================================

def create_dim_shops() -> pd.DataFrame:
    """
    Create dim_shops by merging id_business (active shops) with full_shop_infos (metadata).

    WHY: id_business contains the 161 active shops with MongoDB ObjectIds.
         full_shop_infos contains management hierarchy (KAM, RSM, language).
         We merge to get both: clean IDs + rich metadata.
    """
    print_section("CREATING dim_shops")

    # Load sources
    id_biz = pd.read_csv(BASE_PATH / FILES['id_business'])
    shop_info = pd.read_csv(BASE_PATH / FILES['full_shop_infos'])

    rows_before = len(id_biz)
    print(f"id_business: {len(id_biz)} rows")
    print(f"full_shop_infos: {len(shop_info)} rows")

    # Step 1: Clean column names
    id_biz = clean_column_names(id_biz)
    shop_info = clean_column_names(shop_info)

    # Step 2: Filter out CLOSED shops from full_shop_infos
    # WHY: CLOSED = defunct businesses (37.5% of records). Not useful for active analysis.
    shop_info_active = shop_info[shop_info['macro_segment'] != 'CLOSED'].copy()
    log.log('dim_shops', 'FILTER', f"Removed CLOSED shops from shop_info",
            len(shop_info), len(shop_info_active))

    # Step 3: Prepare id_business as the base (these are the active shops)
    dim_shops = id_biz.rename(columns={
        'id': 'shop_id',
        'code': 'mobis_code',
        'name': 'shop_name',
        'full_name': 'shop_full_name'
    }).copy()

    # Normalize MOBIS code to uppercase (id_business has mixed case: mobis467 vs MOBIS467)
    dim_shops['mobis_code'] = dim_shops['mobis_code'].str.upper()

    # Step 4: Prepare shop_info for merge
    # Rename columns to match our schema
    shop_info_enrichment = shop_info_active.rename(columns={
        'aramis_code': 'mobis_code',
        'pos_name': 'pos_name',
        'shop_manager_name': 'manager_name',
        'shop_manager_private_shop_email': 'manager_email',
        'district_key_account_manager_name': 'kam_name',
        'district_key_account_manager_email': 'kam_email',
        'regional_sales_manager_name': 'rsm_name',
        'regional_sales_manager_email': 'rsm_email',
        'iam_language': 'language'
    })

    # Select only columns we need for enrichment
    enrichment_cols = ['mobis_code', 'macro_segment', 'new_mainchain',
                       'manager_name', 'manager_email', 'kam_name', 'kam_email',
                       'rsm_name', 'rsm_email', 'language']
    enrichment_cols = [c for c in enrichment_cols if c in shop_info_enrichment.columns]
    shop_info_enrichment = shop_info_enrichment[enrichment_cols].drop_duplicates(subset=['mobis_code'])

    # Normalize MOBIS code to uppercase for consistent join
    shop_info_enrichment['mobis_code'] = shop_info_enrichment['mobis_code'].str.upper()

    # Step 5: LEFT JOIN to preserve all active shops
    dim_shops = dim_shops.merge(
        shop_info_enrichment,
        on='mobis_code',
        how='left'
    )
    log.log('dim_shops', 'MERGE', f"Enriched with shop_info metadata",
            rows_before, len(dim_shops))

    # Step 6: Infer language from zipcode where missing
    # WHY: 72% of shops lack IAM-Language. Zip code gives reliable regional inference.
    missing_lang_before = dim_shops['language'].isna().sum()
    dim_shops['language'] = dim_shops.apply(
        lambda row: row['language'] if pd.notna(row['language'])
                    else infer_language_from_zip(row['zipcode']),
        axis=1
    )
    missing_lang_after = dim_shops['language'].isna().sum()
    log.log('dim_shops', 'INFER', f"Inferred language from zipcode",
            missing_lang_before, missing_lang_after)

    # Step 7: Final column selection and ordering
    final_columns = [
        'shop_id', 'mobis_code', 'shop_name', 'city', 'address', 'zipcode',
        'macro_segment', 'new_mainchain',
        'manager_name', 'manager_email',
        'kam_name', 'kam_email',
        'rsm_name', 'rsm_email',
        'language'
    ]
    # Only keep columns that exist
    final_columns = [c for c in final_columns if c in dim_shops.columns]
    dim_shops = dim_shops[final_columns]

    print(f"\nFinal dim_shops: {len(dim_shops)} rows × {len(dim_shops.columns)} columns")
    print(f"Columns: {list(dim_shops.columns)}")

    return dim_shops


# =============================================================================
# TABLE 2: fact_google_reviews
# =============================================================================

def create_fact_google_reviews(dim_shops: pd.DataFrame) -> pd.DataFrame:
    """
    Create fact_google_reviews from Google Reviews CSV.

    WHY: Google Reviews contain customer feedback with AI responses.
         We link to dim_shops via Business_ID (MongoDB ObjectId).
    """
    print_section("CREATING fact_google_reviews")

    # Load source
    df = pd.read_csv(BASE_PATH / FILES['google_reviews'])
    rows_before = len(df)
    cols_before = len(df.columns)
    print(f"Loaded: {rows_before} rows × {cols_before} columns")

    # Step 1: Clean column names
    df = clean_column_names(df)

    # Step 2: Drop empty/artifact columns
    # WHY: EDA found 5 empty columns (key_account_manager_email, shop_manager, unnamed_14/15/16)
    empty_cols = df.columns[df.isnull().all()].tolist()
    unnamed_cols = [c for c in df.columns if c.startswith('unnamed')]
    drop_cols = list(set(empty_cols + unnamed_cols))

    if drop_cols:
        df = df.drop(columns=drop_cols)
        log.log('fact_google_reviews', 'DROP_COLS', f"Removed {len(drop_cols)} empty/unnamed columns",
                rows_before, len(df), cols_before, len(df.columns))

    # Step 3: Rename to clean schema
    column_mapping = {
        'business_id': 'shop_id',
        'review_id': 'review_id',
        'timestamp_client_feedback': 'review_timestamp',
        'client_feedback': 'verbatim',
        'client_rating': 'rating',
        'client_name': 'client_name',
        'timestamp_ai_agent_response': 'response_timestamp',
        'ai_agent_response': 'ai_response',
        'shop_name': 'shop_name_raw',  # Keep for reference, redundant with dim
        'correction': 'correction_text',
        'duplicates': 'duplicate_flag',
        'timestamp': 'processing_timestamp'
    }
    df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})

    # Step 4: Parse timestamps
    # WHY: Timestamps are ISO 8601 strings. Need datetime for filtering.
    for col in ['review_timestamp', 'response_timestamp']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', utc=True)

    # Step 5: Drop rows with missing review_id
    # WHY: EDA found 14 rows (0.8%) with missing Review_ID. These are incomplete records.
    missing_id_before = df['review_id'].isna().sum()
    if missing_id_before > 0:
        df = df.dropna(subset=['review_id'])
        log.log('fact_google_reviews', 'DROP_ROWS', f"Removed {missing_id_before} rows with missing review_id",
                rows_before, len(df))

    # Step 6: Convert rating to int
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').astype('Int64')

    # Step 7: Create is_corrected boolean
    # WHY: Correction column has text when AI response was manually corrected
    if 'correction_text' in df.columns:
        df['is_corrected'] = df['correction_text'].notna() & (df['correction_text'] != '')

    # Step 8: Validate shop_id join
    # Check how many reviews link to known shops
    valid_shop_ids = set(dim_shops['shop_id'].dropna())
    df['shop_id_valid'] = df['shop_id'].isin(valid_shop_ids)
    valid_count = df['shop_id_valid'].sum()
    print(f"Shop ID validation: {valid_count}/{len(df)} ({valid_count/len(df)*100:.1f}%) link to dim_shops")

    # Step 9: Final column selection
    final_columns = [
        'review_id', 'shop_id', 'review_timestamp', 'rating', 'verbatim',
        'client_name', 'response_timestamp', 'ai_response',
        'is_corrected', 'correction_text', 'duplicate_flag'
    ]
    final_columns = [c for c in final_columns if c in df.columns]
    df = df[final_columns]

    print(f"\nFinal fact_google_reviews: {len(df)} rows × {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")

    return df


# =============================================================================
# TABLE 3: fact_sms_surveys
# =============================================================================

def create_fact_sms_surveys(dim_shops: pd.DataFrame) -> pd.DataFrame:
    """
    Create fact_sms_surveys from SMS Survey CSV.

    WHY: SMS Surveys contain post-transaction satisfaction data.
         We link to dim_shops via extracted MOBIS code.
    """
    print_section("CREATING fact_sms_surveys")

    # Load source
    df = pd.read_csv(BASE_PATH / FILES['sms_surveys'])
    rows_before = len(df)
    print(f"Loaded: {rows_before} rows × {len(df.columns)} columns")

    # Step 1: Clean column names
    df = clean_column_names(df)

    # Step 2: Rename to clean schema
    column_mapping = {
        'response_date': 'response_date',
        'interaction_date': 'interaction_date',
        'shop_shop_name_aramis_code': 'shop_name_code_raw',
        'shop_vendor': 'vendor_id',
        'satisfaction_score_score_on_scale_from_1_to_5': 'rating',
        'verbatim': 'verbatim',
        'respondent_id': 'survey_id',
        'shop_shop_audiencename': 'audience_type',
        'shop_city': 'city_raw',
        'shop_customer_type': 'customer_type',
        'shop_channel': 'channel',
        'shop_direction': 'direction',
        'shop_mainchain': 'mainchain',
        'shop_case_type': 'case_type',
        'shop_case_level_1': 'case_level_1',
        'shop_case_level_2': 'case_level_2',
        'shop_case_level_3': 'case_level_3',
        'shop_source_file': 'source_system'
    }
    df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})

    # Step 3: Extract MOBIS code from shop_name_code_raw
    # WHY: SMS data embeds MOBIS code in "SHOP NAME - MOBIS###" format
    df['mobis_code'] = df['shop_name_code_raw'].apply(extract_mobis_code)
    extracted = df['mobis_code'].notna().sum()
    log.log('fact_sms_surveys', 'EXTRACT', f"Extracted MOBIS code from shop name",
            rows_before, extracted)
    print(f"  Extracted: {extracted}/{len(df)} ({extracted/len(df)*100:.1f}%)")

    # Step 4: Map mobis_code to shop_id via dim_shops
    # WHY: We need consistent shop_id (MongoDB ObjectId) to join with Google Reviews
    mobis_to_shop = dim_shops.set_index('mobis_code')['shop_id'].to_dict()
    df['shop_id'] = df['mobis_code'].map(mobis_to_shop)

    mapped = df['shop_id'].notna().sum()
    log.log('fact_sms_surveys', 'MAP', f"Mapped MOBIS to shop_id",
            extracted, mapped)
    print(f"  Mapped to shop_id: {mapped}/{len(df)} ({mapped/len(df)*100:.1f}%)")

    # Step 5: Parse dates
    # WHY: Dates are DD/MM/YYYY format. Need proper date type.
    for col in ['response_date', 'interaction_date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', errors='coerce')

    # Step 6: Convert rating to int
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').astype('Int64')

    # Step 7: Flag unmappable records (687 from Carrefour, SMART, etc.)
    # WHY: These are valid feedback from non-MOBIS shops. Keep with NULL shop_id.
    df['is_mappable'] = df['shop_id'].notna()
    unmapped = (~df['is_mappable']).sum()
    print(f"  Unmappable records (kept with NULL shop_id): {unmapped}")

    # Step 8: Final column selection
    final_columns = [
        'survey_id', 'shop_id', 'mobis_code', 'interaction_date', 'response_date',
        'rating', 'verbatim', 'vendor_id',
        'audience_type', 'customer_type', 'channel', 'case_type',
        'case_level_1', 'case_level_2', 'case_level_3',
        'source_system', 'is_mappable'
    ]
    final_columns = [c for c in final_columns if c in df.columns]
    df = df[final_columns]

    print(f"\nFinal fact_sms_surveys: {len(df)} rows × {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")

    return df


# =============================================================================
# MAIN
# =============================================================================

def main():
    print_section("ORANGE CX INTELLIGENCE - DATA CLEANING PIPELINE")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output directory: {OUTPUT_PATH}")

    # Create tables in order (dim first, then facts)
    dim_shops = create_dim_shops()
    fact_google_reviews = create_fact_google_reviews(dim_shops)
    fact_sms_surveys = create_fact_sms_surveys(dim_shops)

    # Save outputs
    print_section("SAVING CLEAN TABLES")

    dim_shops.to_csv(OUTPUT_PATH / 'dim_shops.csv', index=False)
    print(f"✓ dim_shops.csv: {len(dim_shops)} rows")

    fact_google_reviews.to_csv(OUTPUT_PATH / 'fact_google_reviews.csv', index=False)
    print(f"✓ fact_google_reviews.csv: {len(fact_google_reviews)} rows")

    fact_sms_surveys.to_csv(OUTPUT_PATH / 'fact_sms_surveys.csv', index=False)
    print(f"✓ fact_sms_surveys.csv: {len(fact_sms_surveys)} rows")

    # Save cleaning log
    log_df = log.to_dataframe()
    log_df.to_csv(OUTPUT_PATH / 'cleaning_log.csv', index=False)
    print(f"✓ cleaning_log.csv: {len(log_df)} operations")

    # Print summary
    print_section("CLEANING SUMMARY")

    print("Final Tables:")
    print(f"  dim_shops:           {len(dim_shops):>6,} rows × {len(dim_shops.columns):>2} columns")
    print(f"  fact_google_reviews: {len(fact_google_reviews):>6,} rows × {len(fact_google_reviews.columns):>2} columns")
    print(f"  fact_sms_surveys:    {len(fact_sms_surveys):>6,} rows × {len(fact_sms_surveys.columns):>2} columns")

    print("\nJoin Coverage:")
    gr_joined = fact_google_reviews['shop_id'].notna().sum()
    sms_joined = fact_sms_surveys['shop_id'].notna().sum()
    print(f"  Google Reviews → dim_shops: {gr_joined}/{len(fact_google_reviews)} ({gr_joined/len(fact_google_reviews)*100:.1f}%)")
    print(f"  SMS Surveys → dim_shops:    {sms_joined}/{len(fact_sms_surveys)} ({sms_joined/len(fact_sms_surveys)*100:.1f}%)")

    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == '__main__':
    main()
