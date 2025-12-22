#!/usr/bin/env python3
"""
Data Validation Script: Orange CX Intelligence
===============================================
Quality gate for clean tables before BigQuery load.

Validates 4 dimensions:
1. COMPLETENESS - Required fields present
2. UNIQUENESS - Primary keys unique, foreign keys valid
3. VALIDITY - Values in allowed ranges
4. CONSISTENCY - Cross-field logic holds

Pass threshold: 95% per dimension (configurable)

Usage:
    uv run python validate_orange_cx.py
    uv run python validate_orange_cx.py --threshold 0.99
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Callable
import argparse

# =============================================================================
# CONFIGURATION
# =============================================================================

CLEAN_PATH = Path(__file__).parent / 'clean_output'
OUTPUT_PATH = Path(__file__).parent / 'validation_output'
OUTPUT_PATH.mkdir(exist_ok=True)

DEFAULT_THRESHOLD = 0.95  # 95% pass rate required

# =============================================================================
# VALIDATION FRAMEWORK
# =============================================================================

@dataclass
class ValidationResult:
    """Result of a single validation check."""
    check_name: str
    dimension: str  # COMPLETENESS, UNIQUENESS, VALIDITY, CONSISTENCY
    table: str
    passed: int
    failed: int
    total: int
    details: str = ""

    @property
    def pass_rate(self) -> float:
        return self.passed / self.total if self.total > 0 else 1.0

    @property
    def is_pass(self) -> bool:
        return self.failed == 0


@dataclass
class ValidationReport:
    """Aggregated validation results."""
    results: list = field(default_factory=list)
    threshold: float = DEFAULT_THRESHOLD

    def add(self, result: ValidationResult):
        self.results.append(result)
        status = "✓" if result.is_pass else "✗"
        rate = f"{result.pass_rate*100:.1f}%"
        print(f"  {status} [{result.dimension}] {result.check_name}: {rate} ({result.failed} failures)")
        if result.details and result.failed > 0:
            print(f"      {result.details}")

    def dimension_score(self, dimension: str) -> float:
        """Calculate pass rate for a dimension."""
        dim_results = [r for r in self.results if r.dimension == dimension]
        if not dim_results:
            return 1.0
        total_passed = sum(r.passed for r in dim_results)
        total_records = sum(r.total for r in dim_results)
        return total_passed / total_records if total_records > 0 else 1.0

    def table_score(self, table: str) -> float:
        """Calculate pass rate for a table."""
        table_results = [r for r in self.results if r.table == table]
        if not table_results:
            return 1.0
        total_passed = sum(r.passed for r in table_results)
        total_records = sum(r.total for r in table_results)
        return total_passed / total_records if total_records > 0 else 1.0

    @property
    def overall_score(self) -> float:
        """Overall pass rate across all checks."""
        if not self.results:
            return 1.0
        total_passed = sum(r.passed for r in self.results)
        total_records = sum(r.total for r in self.results)
        return total_passed / total_records if total_records > 0 else 1.0

    @property
    def is_certified(self) -> bool:
        """True if all dimensions pass threshold."""
        dimensions = set(r.dimension for r in self.results)
        return all(self.dimension_score(d) >= self.threshold for d in dimensions)

    def to_dataframe(self) -> pd.DataFrame:
        """Export results as DataFrame."""
        return pd.DataFrame([
            {
                'table': r.table,
                'dimension': r.dimension,
                'check': r.check_name,
                'passed': r.passed,
                'failed': r.failed,
                'total': r.total,
                'pass_rate': r.pass_rate,
                'details': r.details
            }
            for r in self.results
        ])


# =============================================================================
# VALIDATION CHECKS
# =============================================================================

def check_not_null(df: pd.DataFrame, column: str, table: str) -> ValidationResult:
    """Check that a column has no null values."""
    total = len(df)
    nulls = df[column].isna().sum()
    return ValidationResult(
        check_name=f"{column} not null",
        dimension="COMPLETENESS",
        table=table,
        passed=total - nulls,
        failed=nulls,
        total=total,
        details=f"{nulls} null values" if nulls > 0 else ""
    )


def check_unique(df: pd.DataFrame, column: str, table: str) -> ValidationResult:
    """Check that a column has unique values (primary key check)."""
    total = len(df)
    dupes = df[column].duplicated().sum()
    return ValidationResult(
        check_name=f"{column} unique",
        dimension="UNIQUENESS",
        table=table,
        passed=total - dupes,
        failed=dupes,
        total=total,
        details=f"{dupes} duplicate values" if dupes > 0 else ""
    )


def check_foreign_key(df: pd.DataFrame, column: str, valid_values: set,
                      table: str, allow_null: bool = True) -> ValidationResult:
    """Check that foreign key values exist in reference set."""
    if allow_null:
        mask = df[column].notna()
        subset = df[mask]
    else:
        subset = df

    total = len(subset)
    invalid = (~subset[column].isin(valid_values)).sum()
    return ValidationResult(
        check_name=f"{column} FK valid",
        dimension="UNIQUENESS",
        table=table,
        passed=total - invalid,
        failed=invalid,
        total=total,
        details=f"{invalid} invalid FK references" if invalid > 0 else ""
    )


def check_range(df: pd.DataFrame, column: str, min_val, max_val,
                table: str) -> ValidationResult:
    """Check that numeric values are within expected range."""
    subset = df[df[column].notna()]
    total = len(subset)
    out_of_range = ((subset[column] < min_val) | (subset[column] > max_val)).sum()
    return ValidationResult(
        check_name=f"{column} in [{min_val}, {max_val}]",
        dimension="VALIDITY",
        table=table,
        passed=total - out_of_range,
        failed=out_of_range,
        total=total,
        details=f"{out_of_range} out of range" if out_of_range > 0 else ""
    )


def check_date_range(df: pd.DataFrame, column: str, min_date: str, max_date: str,
                     table: str) -> ValidationResult:
    """Check that dates are within expected range."""
    subset = df[df[column].notna()].copy()
    subset[column] = pd.to_datetime(subset[column], errors='coerce', utc=True)
    subset = subset[subset[column].notna()]

    total = len(subset)
    min_dt = pd.to_datetime(min_date, utc=True)
    max_dt = pd.to_datetime(max_date, utc=True)
    out_of_range = ((subset[column] < min_dt) | (subset[column] > max_dt)).sum()
    return ValidationResult(
        check_name=f"{column} in [{min_date[:10]}, {max_date[:10]}]",
        dimension="VALIDITY",
        table=table,
        passed=total - out_of_range,
        failed=out_of_range,
        total=total,
        details=f"{out_of_range} out of range" if out_of_range > 0 else ""
    )


def check_values_in_set(df: pd.DataFrame, column: str, valid_values: set,
                        table: str) -> ValidationResult:
    """Check that categorical values are in allowed set."""
    subset = df[df[column].notna()]
    total = len(subset)
    invalid = (~subset[column].isin(valid_values)).sum()
    return ValidationResult(
        check_name=f"{column} values valid",
        dimension="VALIDITY",
        table=table,
        passed=total - invalid,
        failed=invalid,
        total=total,
        details=f"{invalid} invalid values" if invalid > 0 else ""
    )


def check_distribution_not_constant(df: pd.DataFrame, column: str, table: str,
                                     max_single_value_pct: float = 0.99) -> ValidationResult:
    """Check that a column isn't constant (>99% same value)."""
    subset = df[df[column].notna()]
    total = len(subset)

    if total == 0:
        return ValidationResult(
            check_name=f"{column} distribution varies",
            dimension="CONSISTENCY",
            table=table,
            passed=0, failed=0, total=0,
            details="No non-null values"
        )

    mode_count = subset[column].value_counts().iloc[0]
    mode_pct = mode_count / total

    if mode_pct > max_single_value_pct:
        return ValidationResult(
            check_name=f"{column} distribution varies",
            dimension="CONSISTENCY",
            table=table,
            passed=0, failed=total, total=total,
            details=f"{mode_pct*100:.1f}% same value (suspiciously uniform)"
        )

    return ValidationResult(
        check_name=f"{column} distribution varies",
        dimension="CONSISTENCY",
        table=table,
        passed=total, failed=0, total=total
    )


def check_temporal_order(df: pd.DataFrame, before_col: str, after_col: str,
                         table: str) -> ValidationResult:
    """Check that timestamp A <= timestamp B."""
    subset = df[df[before_col].notna() & df[after_col].notna()].copy()
    subset[before_col] = pd.to_datetime(subset[before_col], errors='coerce', utc=True)
    subset[after_col] = pd.to_datetime(subset[after_col], errors='coerce', utc=True)
    subset = subset[subset[before_col].notna() & subset[after_col].notna()]

    total = len(subset)
    violations = (subset[before_col] > subset[after_col]).sum()
    return ValidationResult(
        check_name=f"{before_col} <= {after_col}",
        dimension="CONSISTENCY",
        table=table,
        passed=total - violations,
        failed=violations,
        total=total,
        details=f"{violations} temporal violations" if violations > 0 else ""
    )


def check_column_names_valid(df: pd.DataFrame, table: str) -> ValidationResult:
    """Check that column names are valid BigQuery identifiers."""
    import re
    pattern = re.compile(r'^[a-z][a-z0-9_]*$')
    total = len(df.columns)
    invalid = [c for c in df.columns if not pattern.match(c)]
    return ValidationResult(
        check_name="column names BigQuery-safe",
        dimension="VALIDITY",
        table=table,
        passed=total - len(invalid),
        failed=len(invalid),
        total=total,
        details=f"Invalid: {invalid}" if invalid else ""
    )


# =============================================================================
# TABLE-SPECIFIC VALIDATION
# =============================================================================

def validate_dim_shops(df: pd.DataFrame, report: ValidationReport):
    """Validate dim_shops table."""
    print("\n--- Validating dim_shops ---")

    # Schema
    report.add(check_column_names_valid(df, "dim_shops"))

    # Completeness
    report.add(check_not_null(df, "shop_id", "dim_shops"))
    report.add(check_not_null(df, "mobis_code", "dim_shops"))
    report.add(check_not_null(df, "shop_name", "dim_shops"))

    # Uniqueness
    report.add(check_unique(df, "shop_id", "dim_shops"))
    report.add(check_unique(df, "mobis_code", "dim_shops"))

    # Validity
    if 'language' in df.columns:
        report.add(check_values_in_set(df, "language", {"NL", "FR", "BI"}, "dim_shops"))


def validate_fact_google_reviews(df: pd.DataFrame, report: ValidationReport,
                                  valid_shop_ids: set):
    """Validate fact_google_reviews table."""
    print("\n--- Validating fact_google_reviews ---")

    # Schema
    report.add(check_column_names_valid(df, "fact_google_reviews"))

    # Completeness
    report.add(check_not_null(df, "review_id", "fact_google_reviews"))
    report.add(check_not_null(df, "shop_id", "fact_google_reviews"))
    report.add(check_not_null(df, "rating", "fact_google_reviews"))

    # Uniqueness
    report.add(check_unique(df, "review_id", "fact_google_reviews"))
    report.add(check_foreign_key(df, "shop_id", valid_shop_ids, "fact_google_reviews",
                                  allow_null=False))

    # Validity
    report.add(check_range(df, "rating", 1, 5, "fact_google_reviews"))
    report.add(check_date_range(df, "review_timestamp", "2025-01-01", "2025-12-31",
                                 "fact_google_reviews"))

    # Consistency
    report.add(check_distribution_not_constant(df, "rating", "fact_google_reviews"))
    if 'response_timestamp' in df.columns:
        report.add(check_temporal_order(df, "review_timestamp", "response_timestamp",
                                         "fact_google_reviews"))


def validate_fact_sms_surveys(df: pd.DataFrame, report: ValidationReport,
                               valid_shop_ids: set):
    """Validate fact_sms_surveys table."""
    print("\n--- Validating fact_sms_surveys ---")

    # Schema
    report.add(check_column_names_valid(df, "fact_sms_surveys"))

    # Completeness
    report.add(check_not_null(df, "survey_id", "fact_sms_surveys"))
    report.add(check_not_null(df, "rating", "fact_sms_surveys"))
    # Note: shop_id CAN be null (unmapped records)

    # Uniqueness
    report.add(check_unique(df, "survey_id", "fact_sms_surveys"))
    # FK check only for records that have shop_id
    report.add(check_foreign_key(df, "shop_id", valid_shop_ids, "fact_sms_surveys",
                                  allow_null=True))

    # Validity
    report.add(check_range(df, "rating", 1, 5, "fact_sms_surveys"))
    report.add(check_date_range(df, "interaction_date", "2025-01-01", "2025-12-31",
                                 "fact_sms_surveys"))
    report.add(check_date_range(df, "response_date", "2025-01-01", "2025-12-31",
                                 "fact_sms_surveys"))

    # Consistency
    report.add(check_distribution_not_constant(df, "rating", "fact_sms_surveys"))
    report.add(check_temporal_order(df, "interaction_date", "response_date",
                                     "fact_sms_surveys"))


# =============================================================================
# MAIN
# =============================================================================

def print_section(title: str):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def main(threshold: float = DEFAULT_THRESHOLD):
    print_section("ORANGE CX INTELLIGENCE - DATA VALIDATION GATE")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Threshold: {threshold*100:.0f}% per dimension")

    # Load tables
    print_section("LOADING TABLES")
    dim_shops = pd.read_csv(CLEAN_PATH / 'dim_shops.csv')
    fact_google_reviews = pd.read_csv(CLEAN_PATH / 'fact_google_reviews.csv')
    fact_sms_surveys = pd.read_csv(CLEAN_PATH / 'fact_sms_surveys.csv')

    print(f"dim_shops: {len(dim_shops):,} rows")
    print(f"fact_google_reviews: {len(fact_google_reviews):,} rows")
    print(f"fact_sms_surveys: {len(fact_sms_surveys):,} rows")

    # Initialize report
    report = ValidationReport(threshold=threshold)
    valid_shop_ids = set(dim_shops['shop_id'].dropna())

    # Run validations
    print_section("RUNNING VALIDATION CHECKS")
    validate_dim_shops(dim_shops, report)
    validate_fact_google_reviews(fact_google_reviews, report, valid_shop_ids)
    validate_fact_sms_surveys(fact_sms_surveys, report, valid_shop_ids)

    # Summary
    print_section("VALIDATION SUMMARY")

    # By dimension
    print("\nBy Dimension:")
    for dim in ["COMPLETENESS", "UNIQUENESS", "VALIDITY", "CONSISTENCY"]:
        score = report.dimension_score(dim)
        status = "✓" if score >= threshold else "✗"
        print(f"  {status} {dim}: {score*100:.1f}%")

    # By table
    print("\nBy Table:")
    for table in ["dim_shops", "fact_google_reviews", "fact_sms_surveys"]:
        score = report.table_score(table)
        status = "✓" if score >= threshold else "✗"
        print(f"  {status} {table}: {score*100:.1f}%")

    # Overall
    print(f"\nOverall Score: {report.overall_score*100:.1f}%")

    # Certification
    print_section("CERTIFICATION")
    if report.is_certified:
        print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║   ✓ DATA QUALITY CERTIFIED                                 ║
    ║                                                            ║
    ║   All dimensions pass threshold.                           ║
    ║   Data is approved for BigQuery load.                      ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
        """)
    else:
        print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║   ✗ CERTIFICATION FAILED                                   ║
    ║                                                            ║
    ║   One or more dimensions below threshold.                  ║
    ║   Review failed checks and fix issues.                     ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
        """)

    # Save results
    print_section("SAVING RESULTS")
    results_df = report.to_dataframe()
    results_df.to_csv(OUTPUT_PATH / 'validation_results.csv', index=False)
    print(f"✓ validation_results.csv: {len(results_df)} checks")

    # Failed checks detail
    failed = results_df[results_df['failed'] > 0]
    if len(failed) > 0:
        failed.to_csv(OUTPUT_PATH / 'validation_failures.csv', index=False)
        print(f"✓ validation_failures.csv: {len(failed)} failed checks")

    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate clean data tables')
    parser.add_argument('--threshold', type=float, default=DEFAULT_THRESHOLD,
                        help=f'Pass threshold (default: {DEFAULT_THRESHOLD})')
    args = parser.parse_args()

    main(threshold=args.threshold)
