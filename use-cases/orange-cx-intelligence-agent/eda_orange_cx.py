#!/usr/bin/env python3
"""
EDA Script for Orange CX Intelligence
=====================================
Exploratory Data Analysis for customer feedback data (Google Reviews + SMS Surveys).

WHY: EDA before cleaning reveals data quality issues, patterns, and informs
     cleaning decisions. We diagnose before we treat.

Usage:
    uv run python eda_orange_cx.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import json
from datetime import datetime

warnings.filterwarnings('ignore')

# Configure pandas display
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_colwidth', 80)

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_PATH = Path(__file__).parent / 'DB'
OUTPUT_PATH = Path(__file__).parent / 'eda_output'
OUTPUT_PATH.mkdir(exist_ok=True)

FILES = {
    'google_reviews': 'orange-cx-intelligence-db - google-review-ai-answers.csv',
    'sms_surveys': 'orange-cx-intelligence-db - sms-client-feedback.csv',
    'id_business': 'orange-cx-intelligence-db - id-business.csv',
    'full_shop_infos': 'orange-cx-intelligence-db - full-shop-infos.csv'
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def analyze_column(series: pd.Series, col_name: str) -> dict:
    """Analyze a single column and return stats."""
    stats = {
        'column': col_name,
        'dtype': str(series.dtype),
        'non_null': int(series.notna().sum()),
        'null_count': int(series.isna().sum()),
        'null_pct': round(series.isna().mean() * 100, 2),
        'unique': int(series.nunique()),
        'unique_pct': round(series.nunique() / len(series) * 100, 2) if len(series) > 0 else 0,
    }

    if pd.api.types.is_numeric_dtype(series):
        clean = series.dropna()
        if len(clean) > 0:
            stats['mean'] = round(clean.mean(), 2)
            stats['std'] = round(clean.std(), 2)
            stats['min'] = clean.min()
            stats['max'] = clean.max()
            stats['median'] = clean.median()
            # Outlier detection (IQR)
            Q1, Q3 = clean.quantile(0.25), clean.quantile(0.75)
            IQR = Q3 - Q1
            outliers = clean[(clean < Q1 - 1.5*IQR) | (clean > Q3 + 1.5*IQR)]
            stats['outlier_count'] = len(outliers)
            stats['outlier_pct'] = round(len(outliers) / len(clean) * 100, 2)
    else:
        # Categorical analysis
        if series.notna().any():
            mode = series.mode()
            stats['mode'] = str(mode.iloc[0]) if not mode.empty else None
            stats['mode_freq'] = round((series == stats['mode']).mean() * 100, 2) if stats['mode'] else 0

            # Check for whitespace issues
            if series.dtype == 'object':
                str_series = series.dropna().astype(str)
                stats['has_leading_space'] = str_series.str.startswith(' ').any()
                stats['has_trailing_space'] = str_series.str.endswith(' ').any()
                stats['case_inconsistent'] = str_series.str.lower().nunique() < str_series.nunique()

    return stats


def analyze_dataframe(df: pd.DataFrame, name: str) -> dict:
    """Comprehensive analysis of a dataframe."""
    results = {
        'name': name,
        'rows': len(df),
        'columns': len(df.columns),
        'memory_mb': round(df.memory_usage(deep=True).sum() / 1e6, 2),
        'duplicate_rows': int(df.duplicated().sum()),
        'complete_rows': int(len(df.dropna())),
        'complete_rows_pct': round(len(df.dropna()) / len(df) * 100, 2) if len(df) > 0 else 0,
        'column_stats': []
    }

    # Analyze each column
    for col in df.columns:
        stats = analyze_column(df[col], col)
        results['column_stats'].append(stats)

    return results


# =============================================================================
# MAIN EDA
# =============================================================================

def main():
    print_section("ORANGE CX INTELLIGENCE - EXPLORATORY DATA ANALYSIS")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output directory: {OUTPUT_PATH}")

    # -------------------------------------------------------------------------
    # PHASE 1: DATA LOADING & OVERVIEW
    # -------------------------------------------------------------------------
    print_section("PHASE 1: DATA LOADING & OVERVIEW")

    dfs = {}
    all_results = {}

    for name, filename in FILES.items():
        filepath = BASE_PATH / filename
        try:
            df = pd.read_csv(filepath)
            dfs[name] = df
            print(f"✓ {name}: {len(df):,} rows × {len(df.columns)} columns")

            # Analyze
            results = analyze_dataframe(df, name)
            all_results[name] = results

        except Exception as e:
            print(f"✗ {name}: Error - {e}")

    # Summary table
    print("\n--- OVERVIEW SUMMARY ---")
    summary_data = []
    for name, res in all_results.items():
        summary_data.append({
            'Dataset': name,
            'Rows': res['rows'],
            'Columns': res['columns'],
            'Memory (MB)': res['memory_mb'],
            'Duplicates': res['duplicate_rows'],
            'Complete %': res['complete_rows_pct']
        })
    summary_df = pd.DataFrame(summary_data)
    print(summary_df.to_string(index=False))

    # -------------------------------------------------------------------------
    # PHASE 2: COLUMN-LEVEL ANALYSIS
    # -------------------------------------------------------------------------
    print_section("PHASE 2: COLUMN-LEVEL ANALYSIS")

    for name, df in dfs.items():
        print(f"\n--- {name.upper()} ---")
        print(f"Columns: {list(df.columns)}\n")

        # Data types
        print("Data Types:")
        print(df.dtypes.value_counts().to_string())

        # First few rows
        print(f"\nFirst 3 rows (transposed for readability):")
        print(df.head(3).T.to_string())

    # -------------------------------------------------------------------------
    # PHASE 3: MISSING VALUE ANALYSIS
    # -------------------------------------------------------------------------
    print_section("PHASE 3: MISSING VALUE ANALYSIS")

    for name, df in dfs.items():
        print(f"\n--- {name.upper()} ---")

        missing = df.isnull().sum()
        missing_pct = (missing / len(df) * 100).round(2)

        missing_df = pd.DataFrame({
            'column': missing.index,
            'missing': missing.values,
            'missing_pct': missing_pct.values
        })
        missing_df = missing_df[missing_df['missing'] > 0].sort_values('missing_pct', ascending=False)

        if len(missing_df) == 0:
            print("No missing values!")
        else:
            print(f"Columns with missing: {len(missing_df)}/{len(df.columns)}")
            print(missing_df.to_string(index=False))

    # -------------------------------------------------------------------------
    # PHASE 4: DUPLICATE ANALYSIS
    # -------------------------------------------------------------------------
    print_section("PHASE 4: DUPLICATE ANALYSIS")

    for name, df in dfs.items():
        print(f"\n--- {name.upper()} ---")

        exact_dupes = df.duplicated().sum()
        print(f"Exact duplicate rows: {exact_dupes}")

        # Check potential ID columns
        for col in df.columns:
            if 'id' in col.lower() or col.lower() in ['id', 'code', 'review_id', 'respondent id']:
                unique = df[col].nunique()
                total = len(df)
                if unique < total:
                    print(f"  Warning: '{col}' has {unique} unique vs {total} rows ({unique/total*100:.1f}%)")

    # -------------------------------------------------------------------------
    # PHASE 5: DATA TYPE ISSUES
    # -------------------------------------------------------------------------
    print_section("PHASE 5: DATA TYPE ISSUES")

    for name, df in dfs.items():
        print(f"\n--- {name.upper()} ---")
        issues = []

        for col in df.columns:
            dtype = str(df[col].dtype)

            # Check for dates stored as strings
            if 'date' in col.lower() or 'timestamp' in col.lower():
                if dtype == 'object':
                    issues.append(f"  '{col}': Date column stored as object (string)")

            # Check for numeric stored as strings
            if dtype == 'object':
                sample = df[col].dropna().head(100)
                try:
                    numeric_test = pd.to_numeric(sample, errors='coerce')
                    if numeric_test.notna().mean() > 0.9:  # >90% can be converted
                        issues.append(f"  '{col}': Possibly numeric, stored as object")
                except:
                    pass

        if issues:
            print("\n".join(issues))
        else:
            print("No obvious type issues detected")

    # -------------------------------------------------------------------------
    # PHASE 6: CATEGORICAL VALUE ANALYSIS
    # -------------------------------------------------------------------------
    print_section("PHASE 6: CATEGORICAL VALUE ANALYSIS")

    for name, df in dfs.items():
        print(f"\n--- {name.upper()} ---")

        cat_cols = df.select_dtypes(include=['object']).columns
        for col in cat_cols[:10]:  # Limit to first 10 for readability
            unique = df[col].nunique()
            if unique <= 20:  # Only show value counts for low cardinality
                print(f"\n{col} ({unique} unique):")
                vc = df[col].value_counts(dropna=False).head(10)
                for val, count in vc.items():
                    pct = count / len(df) * 100
                    val_display = str(val)[:40] + '...' if len(str(val)) > 40 else str(val)
                    print(f"  {val_display}: {count} ({pct:.1f}%)")
            else:
                print(f"\n{col}: {unique} unique values (high cardinality)")

    # -------------------------------------------------------------------------
    # PHASE 7: NUMERIC DISTRIBUTION ANALYSIS
    # -------------------------------------------------------------------------
    print_section("PHASE 7: NUMERIC DISTRIBUTION ANALYSIS")

    for name, df in dfs.items():
        print(f"\n--- {name.upper()} ---")

        num_cols = df.select_dtypes(include=[np.number]).columns
        if len(num_cols) == 0:
            print("No numeric columns")
            continue

        for col in num_cols:
            series = df[col].dropna()
            if len(series) == 0:
                continue

            print(f"\n{col}:")
            print(f"  Count: {len(series):,}")
            print(f"  Mean: {series.mean():.2f} | Median: {series.median():.2f} | Std: {series.std():.2f}")
            print(f"  Min: {series.min()} | Max: {series.max()}")
            print(f"  Q1: {series.quantile(0.25):.2f} | Q3: {series.quantile(0.75):.2f}")

            # Check for suspicious patterns
            if series.min() == series.max():
                print(f"  ⚠️ CONSTANT VALUE!")
            if (series < 0).any():
                print(f"  ⚠️ Contains negative values: {(series < 0).sum()}")

    # -------------------------------------------------------------------------
    # PHASE 8: SHOP ID JOIN ANALYSIS
    # -------------------------------------------------------------------------
    print_section("PHASE 8: SHOP ID JOIN ANALYSIS")

    print("WHY: We need to understand how to join these datasets on shop identifiers")

    # Analyze shop identifiers across datasets
    if 'id_business' in dfs:
        print("\n--- id_business (master shop list) ---")
        id_biz = dfs['id_business']
        print(f"Unique 'id' values: {id_biz['id'].nunique()}")
        print(f"Unique 'code' values: {id_biz['code'].nunique()}")
        print(f"Sample 'id': {id_biz['id'].iloc[0]}")
        print(f"Sample 'code': {id_biz['code'].iloc[0]}")

    if 'full_shop_infos' in dfs:
        print("\n--- full_shop_infos ---")
        shop_info = dfs['full_shop_infos']
        if 'Aramis code' in shop_info.columns:
            print(f"Unique 'Aramis code' values: {shop_info['Aramis code'].nunique()}")
            print(f"Sample 'Aramis code': {shop_info['Aramis code'].dropna().iloc[0] if shop_info['Aramis code'].notna().any() else 'N/A'}")

    if 'google_reviews' in dfs:
        print("\n--- google_reviews ---")
        gr = dfs['google_reviews']
        if 'Business_ID' in gr.columns:
            print(f"Unique 'Business_ID' values: {gr['Business_ID'].nunique()}")
            print(f"Sample 'Business_ID': {gr['Business_ID'].iloc[0]}")

    if 'sms_surveys' in dfs:
        print("\n--- sms_surveys ---")
        sms = dfs['sms_surveys']
        shop_col = [c for c in sms.columns if 'shop name' in c.lower()]
        if shop_col:
            col = shop_col[0]
            print(f"Column: '{col}'")
            print(f"Sample values:")
            for val in sms[col].dropna().head(5):
                print(f"  {val}")

            # Try to extract MOBIS codes
            print("\nAttempting MOBIS code extraction:")
            sample = sms[col].dropna().str.extract(r'(MOBIS\d+)', expand=False)
            print(f"  Extracted codes: {sample.notna().sum()} / {len(sample)}")
            if sample.notna().any():
                print(f"  Sample extracted: {sample.dropna().iloc[:3].tolist()}")

    # -------------------------------------------------------------------------
    # PHASE 9: DATE/TIME ANALYSIS
    # -------------------------------------------------------------------------
    print_section("PHASE 9: DATE/TIME ANALYSIS")

    for name, df in dfs.items():
        print(f"\n--- {name.upper()} ---")

        date_cols = [c for c in df.columns if 'date' in c.lower() or 'timestamp' in c.lower()]
        if not date_cols:
            print("No date/time columns detected")
            continue

        for col in date_cols:
            print(f"\n{col}:")
            sample = df[col].dropna().head(5).tolist()
            print(f"  Sample values: {sample}")

            # Try to parse and get range
            try:
                parsed = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
                valid = parsed.notna().sum()
                print(f"  Parseable: {valid}/{len(df)} ({valid/len(df)*100:.1f}%)")
                if valid > 0:
                    print(f"  Min: {parsed.min()}")
                    print(f"  Max: {parsed.max()}")
            except Exception as e:
                print(f"  Parse error: {e}")

    # -------------------------------------------------------------------------
    # PHASE 10: QUALITY ISSUES SUMMARY
    # -------------------------------------------------------------------------
    print_section("PHASE 10: QUALITY ISSUES SUMMARY")

    issues = []

    # Check each dataset
    for name, df in dfs.items():
        # Missing values
        high_missing = df.isnull().mean()
        for col in high_missing[high_missing > 0.5].index:
            issues.append({
                'Dataset': name,
                'Issue': f"High missing: {col}",
                'Severity': 'Major',
                'Records': f"{df[col].isnull().sum()}/{len(df)}",
                'Action': 'Consider drop or investigate'
            })

        # Duplicates
        if df.duplicated().sum() > 0:
            issues.append({
                'Dataset': name,
                'Issue': 'Exact duplicate rows',
                'Severity': 'Major',
                'Records': str(df.duplicated().sum()),
                'Action': 'Deduplicate'
            })

        # Empty columns
        empty_cols = df.columns[df.isnull().all()].tolist()
        for col in empty_cols:
            issues.append({
                'Dataset': name,
                'Issue': f"Empty column: {col}",
                'Severity': 'Minor',
                'Records': str(len(df)),
                'Action': 'Drop column'
            })

    if issues:
        issues_df = pd.DataFrame(issues)
        print(issues_df.to_string(index=False))
    else:
        print("No critical issues found")

    # -------------------------------------------------------------------------
    # SAVE RESULTS
    # -------------------------------------------------------------------------
    print_section("SAVING RESULTS")

    # Save column summaries
    for name, results in all_results.items():
        col_df = pd.DataFrame(results['column_stats'])
        col_df.to_csv(OUTPUT_PATH / f'{name}_columns.csv', index=False)
        print(f"Saved: {name}_columns.csv")

    # Save issues
    if issues:
        issues_df.to_csv(OUTPUT_PATH / 'quality_issues.csv', index=False)
        print("Saved: quality_issues.csv")

    print(f"\nEDA Complete! Results in: {OUTPUT_PATH}")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == '__main__':
    main()
