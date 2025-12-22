# Python Code for LLM Context Generation

## Overview

These patterns help extract schema information and generate LLM context documents from clean data files.

---

## Schema Extraction

### Basic Schema from DataFrame

```python
import pandas as pd
from typing import Dict, List, Any

def extract_schema(df: pd.DataFrame, table_name: str) -> Dict[str, Any]:
    """Extract schema information from a DataFrame."""
    schema = {
        'table_name': table_name,
        'row_count': len(df),
        'columns': []
    }

    for col in df.columns:
        col_info = {
            'name': col,
            'dtype': str(df[col].dtype),
            'null_count': int(df[col].isna().sum()),
            'null_pct': round(100 * df[col].isna().sum() / len(df), 1),
            'unique_count': int(df[col].nunique()),
            'sample_values': df[col].dropna().head(3).tolist()
        }

        # Add type-specific info
        if pd.api.types.is_numeric_dtype(df[col]):
            col_info['min'] = df[col].min()
            col_info['max'] = df[col].max()
            col_info['mean'] = round(df[col].mean(), 2)

        if pd.api.types.is_datetime64_any_dtype(df[col]):
            col_info['min_date'] = str(df[col].min())
            col_info['max_date'] = str(df[col].max())

        # Detect categorical (low cardinality)
        if df[col].nunique() <= 20 and df[col].dtype == 'object':
            col_info['is_categorical'] = True
            col_info['categories'] = df[col].dropna().unique().tolist()

        schema['columns'].append(col_info)

    return schema
```

### Detect Primary Keys

```python
def detect_primary_key(df: pd.DataFrame) -> List[str]:
    """Identify likely primary key columns."""
    pk_candidates = []

    for col in df.columns:
        # Check if unique and non-null
        if df[col].nunique() == len(df) and df[col].isna().sum() == 0:
            pk_candidates.append(col)

    # Prefer columns with 'id' in name
    id_cols = [c for c in pk_candidates if 'id' in c.lower()]
    if id_cols:
        return id_cols[:1]

    return pk_candidates[:1] if pk_candidates else []
```

### Detect Foreign Keys

```python
def detect_foreign_keys(
    df: pd.DataFrame,
    dim_tables: Dict[str, pd.DataFrame]
) -> List[Dict[str, Any]]:
    """Identify likely foreign key relationships."""
    fk_relationships = []

    for col in df.columns:
        if 'id' not in col.lower():
            continue

        for dim_name, dim_df in dim_tables.items():
            # Check if column values exist in dimension table
            for dim_col in dim_df.columns:
                if 'id' not in dim_col.lower():
                    continue

                # Calculate match rate
                df_values = set(df[col].dropna().unique())
                dim_values = set(dim_df[dim_col].dropna().unique())

                if df_values.issubset(dim_values) or len(df_values & dim_values) / len(df_values) > 0.8:
                    match_rate = len(df_values & dim_values) / len(df_values)
                    null_rate = df[col].isna().sum() / len(df)

                    fk_relationships.append({
                        'column': col,
                        'references_table': dim_name,
                        'references_column': dim_col,
                        'match_rate': round(match_rate * 100, 1),
                        'null_rate': round(null_rate * 100, 1)
                    })

    return fk_relationships
```

---

## Coverage Analysis

### Calculate Completeness

```python
def calculate_completeness(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate completeness percentage for each column."""
    return {
        col: round(100 * (1 - df[col].isna().sum() / len(df)), 1)
        for col in df.columns
    }
```

### Identify Data Gaps

```python
def identify_data_gaps(
    fact_df: pd.DataFrame,
    dim_df: pd.DataFrame,
    fact_fk: str,
    dim_pk: str
) -> Dict[str, Any]:
    """Identify records that don't match dimension table."""

    fact_values = set(fact_df[fact_fk].dropna().unique())
    dim_values = set(dim_df[dim_pk].dropna().unique())

    # Values in fact but not in dim
    orphan_values = fact_values - dim_values
    orphan_records = fact_df[fact_df[fact_fk].isin(orphan_values)]

    # NULL foreign keys
    null_fk_records = fact_df[fact_df[fact_fk].isna()]

    return {
        'total_records': len(fact_df),
        'matched_records': len(fact_df[fact_df[fact_fk].isin(dim_values)]),
        'orphan_count': len(orphan_records),
        'orphan_values': list(orphan_values)[:10],  # Sample
        'null_fk_count': len(null_fk_records),
        'match_rate_pct': round(100 * len(fact_df[fact_df[fact_fk].isin(dim_values)]) / len(fact_df), 1)
    }
```

---

## Categorical Value Extraction

### Extract Enum Values

```python
def extract_categorical_values(df: pd.DataFrame, max_cardinality: int = 20) -> Dict[str, List[str]]:
    """Extract unique values from low-cardinality string columns."""
    categorical = {}

    for col in df.columns:
        if df[col].dtype == 'object' and df[col].nunique() <= max_cardinality:
            values = df[col].dropna().unique().tolist()
            categorical[col] = sorted(values)

    return categorical
```

### Generate Value Distribution

```python
def value_distribution(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Generate value distribution for a column."""
    dist = df[column].value_counts(dropna=False).reset_index()
    dist.columns = ['value', 'count']
    dist['pct'] = round(100 * dist['count'] / len(df), 1)
    return dist
```

---

## Temporal Boundary Detection

```python
def detect_temporal_boundaries(df: pd.DataFrame) -> Dict[str, Dict[str, str]]:
    """Find date ranges for all datetime columns."""
    boundaries = {}

    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            boundaries[col] = {
                'min': str(df[col].min().date()) if pd.notna(df[col].min()) else None,
                'max': str(df[col].max().date()) if pd.notna(df[col].max()) else None,
                'span_days': (df[col].max() - df[col].min()).days if pd.notna(df[col].min()) else None
            }

    return boundaries
```

---

## Markdown Generation

### Generate Schema Markdown

```python
def schema_to_markdown(schema: Dict[str, Any], grain: str) -> str:
    """Convert schema dict to markdown table."""
    lines = [
        f"### {schema['table_name']} ({schema['row_count']:,} rows) — {grain}",
        "",
        "| Column | Type | Meaning | Example | Notes |",
        "|--------|------|---------|---------|-------|"
    ]

    for col in schema['columns']:
        notes = []
        if col['null_pct'] > 0:
            notes.append(f"{col['null_pct']}% NULL")
        if col.get('is_categorical'):
            notes.append(f"Enum: {', '.join(col['categories'][:3])}...")
        if 'min' in col and 'max' in col:
            notes.append(f"Range: {col['min']}-{col['max']}")

        example = str(col['sample_values'][0]) if col['sample_values'] else ''
        example = example[:20] + '...' if len(example) > 20 else example

        lines.append(
            f"| {col['name']} | {col['dtype']} | [meaning] | {example} | {'; '.join(notes) or '-'} |"
        )

    return '\n'.join(lines)
```

### Generate Limits Markdown

```python
def limits_to_markdown(gaps: Dict[str, Dict[str, Any]]) -> str:
    """Convert data gaps to markdown table."""
    lines = [
        "## Data Limits",
        "",
        "| Limitation | Affected Records | Coverage | Impact |",
        "|------------|------------------|----------|--------|"
    ]

    for name, gap in gaps.items():
        lines.append(
            f"| {name} | {gap['orphan_count'] + gap['null_fk_count']:,} | "
            f"{gap['match_rate_pct']}% | Cannot join to dimension |"
        )

    return '\n'.join(lines)
```

---

## Full Context Generator

```python
def generate_llm_context(
    tables: Dict[str, pd.DataFrame],
    grains: Dict[str, str],
    project_name: str
) -> str:
    """Generate complete LLM context document."""

    sections = [
        f"# Data Context: {project_name}",
        "",
        "## TL;DR",
        "",
        f"This dataset contains {len(tables)} tables:",
    ]

    for name, df in tables.items():
        sections.append(f"- **{name}**: {len(df):,} rows — {grains.get(name, 'One row per record')}")

    sections.extend(["", "## Schema Overview", ""])

    for name, df in tables.items():
        schema = extract_schema(df, name)
        sections.append(schema_to_markdown(schema, grains.get(name, 'One row per record')))
        sections.append("")

    # Add relationships
    sections.extend(["## Relationships", "", "```"])
    # ... add relationship detection
    sections.append("```")

    return '\n'.join(sections)
```

---

## Usage Example

```python
# Load clean data
dim_shops = pd.read_csv('clean_output/dim_shops.csv')
fact_reviews = pd.read_csv('clean_output/fact_google_reviews.csv')
fact_surveys = pd.read_csv('clean_output/fact_sms_surveys.csv')

# Define grains
grains = {
    'dim_shops': 'One row per retail location',
    'fact_google_reviews': 'One row per Google review',
    'fact_sms_surveys': 'One row per SMS survey response'
}

# Generate context
context = generate_llm_context(
    tables={
        'dim_shops': dim_shops,
        'fact_google_reviews': fact_reviews,
        'fact_sms_surveys': fact_surveys
    },
    grains=grains,
    project_name='Orange CX Intelligence'
)

# Save
with open('ai-docs/data-llm-orange-cx-intelligence.md', 'w') as f:
    f.write(context)
```

---

## BigQuery Schema Extraction

If data is already in BigQuery:

```python
from google.cloud import bigquery

def extract_bigquery_schema(project: str, dataset: str, table: str) -> Dict[str, Any]:
    """Extract schema from BigQuery table."""
    client = bigquery.Client(project=project)
    table_ref = f"{project}.{dataset}.{table}"
    table_obj = client.get_table(table_ref)

    schema = {
        'table_name': table,
        'row_count': table_obj.num_rows,
        'columns': []
    }

    for field in table_obj.schema:
        schema['columns'].append({
            'name': field.name,
            'dtype': field.field_type,
            'mode': field.mode,  # NULLABLE, REQUIRED, REPEATED
            'description': field.description or ''
        })

    return schema
```

---

## Checklist

When generating LLM context:

- [ ] Extract schema from all tables
- [ ] Detect primary and foreign keys
- [ ] Calculate completeness metrics
- [ ] Identify data gaps and orphans
- [ ] Extract categorical values
- [ ] Detect temporal boundaries
- [ ] Generate markdown documentation
- [ ] Add semantic meanings manually
- [ ] Review and edit generated content
