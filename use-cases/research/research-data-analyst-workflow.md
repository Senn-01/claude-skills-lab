---
topic: "Data Analyst Workflow Best Practices for Claude Code Commands"
date: 2025-12-18T12:00:00Z
status: complete
tools_used: [tavily, context7]
queries_executed: 7
agents_spawned: 4
focus: pre-ML phases (business understanding, EDA, data cleaning)
---

# Research: Data Analyst Workflow Best Practices

## Executive Summary

The CRISP-DM framework defines 6 phases for data projects; the pre-ML phases (Business Understanding → Data Understanding → Data Preparation) form the foundation. Top analysts follow systematic checklists: stakeholder interviews with 5W1H questions, structured EDA with univariate/multivariate analysis, and ordered cleaning pipelines. This research enables creation of Claude Code commands (`/data-understand`, `/data-explore`, `/data-clean`, `/data-validate`) that mirror professional workflows.

## Research Goal

Define the exact phases, techniques, checklists, and deliverables of a professional data analyst workflow for pre-ML stages, enabling creation of Claude Code commands that enforce best practices.

---

## Concept Overview: CRISP-DM Framework

**CRISP-DM** (Cross-Industry Standard Process for Data Mining) is the most commonly used framework for data science projects. It's cyclical and iterative.

### The 6 Phases

| Phase | Focus | Pre-ML? |
|-------|-------|---------|
| 1. Business Understanding | Define objectives, translate to analytics problem | ✓ |
| 2. Data Understanding | Explore data, identify quality issues, form hypotheses | ✓ |
| 3. Data Preparation | Clean, transform, construct final dataset | ✓ |
| 4. Modeling | Select and apply modeling techniques | ✗ |
| 5. Evaluation | Assess model against business objectives | ✗ |
| 6. Deployment | Operationalize insights | ✗ |

**Key insight**: Phases 1-3 are where 80% of time is spent and where most projects fail if done poorly.

---

## Phase 1: Business Understanding

### Purpose
Establish the foundation. A poor business understanding derails entire projects.

### Stakeholder Questions (5W1H Framework)

**Why**
- Why is this analysis needed? Why now?
- What problems are you trying to solve?

**What**
- What would success look like?
- What specific data/outputs are required?
- What actions should the analysis enable?

**Who**
- Who are the stakeholders?
- Who will use the results?
- Who owns the data?

**When**
- What is the timeline?
- When should updates occur?

**Where**
- Where will the solution be deployed?
- Where is data stored?

**How**
- How will insights be operationalized?
- How will we validate results?
- How stable are source systems?

### Checklist

```markdown
## Business Understanding Checklist

### Stakeholder Identification
- [ ] Identify all key stakeholders and their roles
- [ ] Document their specific interests and concerns
- [ ] Establish communication cadence

### Problem Definition
- [ ] Document the business problem in business terms
- [ ] Translate to analytics problem definition
- [ ] Define what decisions this analysis will enable

### Success Criteria
- [ ] Define measurable success criteria
- [ ] Establish KPIs and measurement approach
- [ ] Get stakeholder agreement on criteria

### Constraints & Scope
- [ ] Document timeline and budget
- [ ] Identify technical/organizational constraints
- [ ] Define what's in scope and out of scope

### Data Landscape
- [ ] Identify data sources and availability
- [ ] Assess data access permissions
- [ ] Document data update frequencies

### Sign-off
- [ ] Get stakeholder approval on problem definition
- [ ] Document assumptions and risks
- [ ] Create preliminary project plan
```

### Deliverables

| Artifact | Purpose |
|----------|---------|
| Problem Statement | 1-page business problem definition |
| Stakeholder Register | Who, their interests, communication needs |
| Success Criteria Doc | Measurable KPIs and thresholds |
| Scope Statement | In/out of scope, constraints |
| Data Source Inventory | Available data, access, freshness |

---

## Phase 2: Data Understanding (EDA)

### Purpose
Explore data to understand its properties, identify quality issues, and form hypotheses.

### EDA Checklist

```markdown
## Exploratory Data Analysis Checklist

### 1. Initial Overview
- [ ] Load data and examine first/last rows (`df.head()`, `df.tail()`)
- [ ] Check dimensions (`df.shape`)
- [ ] Review data types (`df.dtypes`, `df.info()`)
- [ ] Generate statistical summary (`df.describe()`)

### 2. Data Profiling
- [ ] Calculate missing value percentages per column
- [ ] Identify pattern in missingness (random vs systematic)
- [ ] Count duplicate records
- [ ] Find constant or near-constant columns
- [ ] Check for class imbalance in target variable

### 3. Univariate Analysis
- [ ] Analyze distribution of each numeric column
- [ ] Check for skewness and outliers
- [ ] Examine value counts for categorical columns
- [ ] Identify columns with high cardinality

### 4. Multivariate Analysis
- [ ] Calculate correlation matrix
- [ ] Identify highly correlated features (>0.8)
- [ ] Explore relationships between features and target
- [ ] Check for multicollinearity

### 5. Data Quality Assessment
- [ ] Document quality issues found
- [ ] Categorize by severity (critical/major/minor)
- [ ] Estimate effort to remediate
- [ ] Update Data Source Inventory with findings
```

### Statistical Techniques

| Technique | When to Use | What It Reveals |
|-----------|-------------|-----------------|
| Descriptive Stats | Always | Central tendency, spread, range |
| Distribution Analysis | Numeric columns | Normality, skewness, modality |
| Correlation (Pearson) | Linear relationships | Strength of linear association |
| Correlation (Spearman) | Non-linear relationships | Monotonic relationships |
| IQR/Z-score | Outlier detection | Anomalous values |

### Visualization Patterns

| Chart | Best For |
|-------|----------|
| Histogram | Distribution of continuous variables |
| Box Plot | Outliers, quartiles, comparing groups |
| Scatter Plot | Relationships between two variables |
| Heatmap | Correlation matrix visualization |
| Bar Chart | Categorical frequencies |
| Pair Plot | All pairwise relationships |

### EDA Code Template

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# === 1. INITIAL OVERVIEW ===
df = pd.read_csv('data.csv')
print("Shape:", df.shape)
print("\nData Types:")
print(df.dtypes)
print("\nStatistical Summary:")
print(df.describe())

# === 2. DATA PROFILING ===
# Missing values
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
print("\nMissing Values:")
print(pd.DataFrame({'count': missing, 'percent': missing_pct}))

# Duplicates
print(f"\nDuplicate rows: {df.duplicated().sum()}")

# === 3. UNIVARIATE ANALYSIS ===
# Numeric distributions
df.hist(figsize=(12, 10), bins=30)
plt.tight_layout()
plt.savefig('distributions.png')

# Categorical value counts
for col in df.select_dtypes(include=['object', 'category']):
    print(f"\n{col}:")
    print(df[col].value_counts().head(10))

# === 4. MULTIVARIATE ANALYSIS ===
# Correlation matrix
numeric_cols = df.select_dtypes(include=[np.number]).columns
corr_matrix = df[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.savefig('correlation_matrix.png')

# High correlations
high_corr = np.where(np.abs(corr_matrix) > 0.8)
high_corr_pairs = [(corr_matrix.index[x], corr_matrix.columns[y], corr_matrix.iloc[x, y])
                   for x, y in zip(*high_corr) if x < y]
print("\nHighly correlated pairs (>0.8):")
for pair in high_corr_pairs:
    print(f"  {pair[0]} - {pair[1]}: {pair[2]:.3f}")

# === 5. OUTLIER DETECTION ===
def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower) | (df[column] > upper)]
    return len(outliers), lower, upper

print("\nOutlier Detection (IQR method):")
for col in numeric_cols:
    count, lower, upper = detect_outliers_iqr(df, col)
    if count > 0:
        print(f"  {col}: {count} outliers (bounds: {lower:.2f} - {upper:.2f})")
```

### Deliverables

| Artifact | Purpose |
|----------|---------|
| EDA Report | Findings, visualizations, quality issues |
| Data Dictionary | Column definitions, types, valid ranges |
| Quality Issues Log | Issues found, severity, remediation plan |
| Correlation Analysis | Key relationships discovered |

---

## Phase 3: Data Preparation (Cleaning)

### Purpose
Transform raw data into clean, analysis-ready dataset.

### Cleaning Pipeline (Ordered Steps)

```markdown
## Data Cleaning Pipeline

### Step 1: Standardize Structure
- [ ] Clean column names (lowercase, underscores, no special chars)
- [ ] Ensure consistent naming conventions
- [ ] Organize column order logically

### Step 2: Handle Data Types
- [ ] Convert columns to appropriate types
- [ ] Fix numbers stored as strings
- [ ] Parse dates correctly
- [ ] Convert categoricals

### Step 3: Handle Missing Values
- [ ] Document missing value strategy per column
- [ ] Apply appropriate imputation/removal
- [ ] Create missingness indicators if needed

### Step 4: Remove Duplicates
- [ ] Identify exact duplicates
- [ ] Identify partial duplicates (key columns)
- [ ] Apply deduplication strategy

### Step 5: Handle Outliers
- [ ] Apply outlier treatment per column
- [ ] Document decisions (remove/cap/transform)

### Step 6: Validate & Verify
- [ ] Re-run data quality checks
- [ ] Verify all constraints satisfied
- [ ] Generate cleaning report

### Step 7: Export Clean Data
- [ ] Save cleaned dataset
- [ ] Document all transformations
- [ ] Version the output
```

### Missing Value Strategies

| Strategy | When to Use | Code |
|----------|-------------|------|
| Drop rows | <5% missing, MCAR | `df.dropna()` |
| Drop column | >50% missing, not critical | `df.drop(columns=['col'])` |
| Mean/Median | Numeric, MAR | `df['col'].fillna(df['col'].median())` |
| Mode | Categorical | `df['col'].fillna(df['col'].mode()[0])` |
| Forward fill | Time series | `df['col'].ffill()` |
| Interpolate | Ordered numeric | `df['col'].interpolate()` |
| Indicator | Missingness is informative | `df['col_missing'] = df['col'].isna()` |

### Outlier Handling

| Method | Detection | Remediation |
|--------|-----------|-------------|
| IQR | `Q1 - 1.5*IQR` to `Q3 + 1.5*IQR` | Remove or cap at bounds |
| Z-score | `abs(z) > 3` | Remove extreme values |
| Domain rules | Business logic | Correct or flag |

```python
# IQR capping
Q1, Q3 = df['col'].quantile([0.25, 0.75])
IQR = Q3 - Q1
lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
df['col'] = df['col'].clip(lower=lower, upper=upper)
```

### Data Type Conversion

```python
# Safe numeric conversion (invalid → NaN)
df['col'] = pd.to_numeric(df['col'], errors='coerce')

# Date parsing
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Category conversion (memory efficient)
df['category_col'] = df['category_col'].astype('category')
```

### Common Gotchas

| Gotcha | Problem | Solution |
|--------|---------|----------|
| Chained assignment | `df[cond]['col'] = val` doesn't work | Use `df.loc[cond, 'col'] = val` |
| Copy vs View | Modifying slice doesn't modify original | Use `.copy()` explicitly |
| Index gaps | After dropping rows, index has gaps | `df.reset_index(drop=True)` |
| Data leakage | Imputing with full dataset stats | Fit on train only |

### Deliverables

| Artifact | Purpose |
|----------|---------|
| Cleaned Dataset | Analysis-ready data file |
| Transformation Log | All changes made, with rationale |
| Cleaning Report | Before/after statistics |
| Data Pipeline Code | Reproducible cleaning script |

---

## Data Quality Assessment

### Quality Dimensions

| Dimension | Definition | How to Measure |
|-----------|------------|----------------|
| Completeness | No missing values | `df.isnull().sum() / len(df)` |
| Accuracy | Values are correct | Domain validation, range checks |
| Consistency | Uniform formats | Cross-field validation |
| Uniqueness | No duplicates | `df.duplicated().sum()` |
| Timeliness | Data is current | Check timestamps |
| Conformity | Matches schema | Type and constraint checks |

### Quality Thresholds

| Metric | Acceptable | Warning | Critical |
|--------|------------|---------|----------|
| Missing rate (critical fields) | <5% | 5-10% | >10% |
| Missing rate (optional fields) | <20% | 20-30% | >30% |
| Duplicate rate | <1% | 1-5% | >5% |
| Format conformity | 100% | 95-100% | <95% |

### Python Quality Tools

| Tool | Use Case |
|------|----------|
| **pandas_dq** | Quick profiling, automated fixing |
| **Great Expectations** | Declarative validation, CI/CD integration |
| **Pandera** | Schema-based validation, type hints |
| **PyDeequ** | Large-scale Spark data quality |

### Quality Check Template

```python
def data_quality_report(df, name="Dataset"):
    """Generate comprehensive data quality report."""
    report = {
        'name': name,
        'rows': len(df),
        'columns': len(df.columns),
        'missing_total': df.isnull().sum().sum(),
        'missing_pct': (df.isnull().sum().sum() / df.size * 100).round(2),
        'duplicates': df.duplicated().sum(),
        'duplicate_pct': (df.duplicated().sum() / len(df) * 100).round(2),
    }

    # Per-column quality
    col_quality = []
    for col in df.columns:
        col_info = {
            'column': col,
            'dtype': str(df[col].dtype),
            'missing': df[col].isnull().sum(),
            'missing_pct': (df[col].isnull().sum() / len(df) * 100).round(2),
            'unique': df[col].nunique(),
            'unique_pct': (df[col].nunique() / len(df) * 100).round(2),
        }
        col_quality.append(col_info)

    report['columns_detail'] = pd.DataFrame(col_quality)
    return report
```

---

## Proposed Command Structure

Based on this research, here are recommended Claude Code commands:

### 1. `/data-understand` - Business Understanding Phase

**Triggers**: Starting a new data project, receiving new data/problem

**Actions**:
1. Present stakeholder questionnaire (5W1H)
2. Generate Problem Statement template
3. Create Scope Document
4. Output: `ai-docs/data-understand-{project}.md`

### 2. `/data-explore` (or `/eda`) - Data Understanding Phase

**Triggers**: After loading dataset, before cleaning

**Actions**:
1. Run EDA checklist automatically
2. Generate visualizations (distributions, correlations)
3. Detect quality issues
4. Output: `ai-docs/eda-report-{dataset}.md`

### 3. `/data-clean` - Data Preparation Phase

**Triggers**: After EDA, ready to clean

**Actions**:
1. Present cleaning pipeline checklist
2. Suggest strategies for each issue found
3. Generate cleaning code
4. Output: cleaned dataset + transformation log

### 4. `/data-validate` (or `/data-quality`) - Quality Assessment

**Triggers**: After cleaning, before analysis/modeling

**Actions**:
1. Run quality dimension checks
2. Compare against thresholds
3. Generate quality report
4. Output: `ai-docs/quality-report-{dataset}.md`

---

## Decision Points

Based on this research, decisions to make:

1. **Command naming**: `/data-understand` vs `/data-problem` vs `/data-scope`
2. **Output location**: `ai-docs/` vs `reports/` vs inline
3. **Automation level**: Fully automated vs checklist-guided
4. **Tool integration**: pandas_dq vs Great Expectations vs custom

---

## Sources

| Source | Type | Insight |
|--------|------|---------|
| CRISP-DM Academic Paper (2024) | Research | Framework evolution, DMAIC integration |
| datascience-pm.com | Guide | 6-phase breakdown, deployment emphasis |
| Applied AI Course | Tutorial | EDA techniques and checklist |
| DataCamp | Tutorial | Data cleaning patterns |
| KDnuggets | Article | 7 essential quality checks |
| pandas.pydata.org (Context7) | Docs | Official API for cleaning functions |
| Bridging the Gap | Guide | 5W1H requirements elicitation |

## Queries Executed

| Query | Tool | Agent | Key Finding |
|-------|------|-------|-------------|
| CRISP-DM phases 2024 | Tavily | Concept | 6-phase cyclical framework |
| Business understanding stakeholder questions | Tavily | Concept | 5W1H framework essential |
| EDA best practices checklist | Tavily | Examples | 5-step systematic process |
| Data cleaning pipeline steps | Tavily | Examples | 7-step ordered pipeline |
| Data quality metrics automated | Tavily | Ecosystem | Quality dimensions + tools |
| Project deliverables per phase | Tavily | Ecosystem | Phase-specific artifacts |
| Pandas data cleaning functions | Context7 | Docs | dropna, fillna, duplicated, astype |

## Open Questions

- How to handle Jupyter notebook integration vs script-based workflows?
- Should commands support incremental/resumable workflows?
- Integration with existing skill-creator methodology for command creation?

## Follow-up Research

[Reserved for follow-up questions]
