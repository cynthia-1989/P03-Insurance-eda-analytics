# P03 ⭐⭐⭐ — Insurance EDA 🛡️

## Overview

This project builds a production-grade insurance exploratory data analysis (EDA) pipeline for analysing insurance claims behaviour, fraud patterns, customer risk profiles, statistical relationships, forecasting, and anomalous insurance activities.

The pipeline loads processed insurance data, performs claim profiling, fraud analysis, statistical hypothesis testing, forecasting, anomaly detection, HTML reporting, and generates visualisations for actuarial and risk analysis.

---

## Table of Contents

1. [Project Brief](#project-brief)
2. [EDA Workflow](#eda-workflow)
3. [Input and Output](#input-and-output)
4. [Project Structure](#project-structure)
5. [Claim Type Analysis](#claim-type-analysis)
6. [Risk Grade Analysis](#risk-grade-analysis)
7. [ANOVA Statistical Test](#anova-statistical-test)
8. [Kruskal-Wallis Test](#kruskal-wallis-test)
9. [Feature Importance Analysis](#feature-importance-analysis)
10. [Forecasting](#forecasting)
11. [Fraud Pattern Analysis](#fraud-pattern-analysis)
12. [Anomaly Detection](#anomaly-detection)
13. [Visualisations](#visualisations)
14. [HTML Reporting](#html-reporting)
15. [How to Run](#how-to-run)
16. [Tests](#tests)
17. [Git Workflow](#git-workflow)

---

## Project Brief

**Company:** Shield Guard Insurance Group  
**Role:** Lead Data Analyst

The insurance dataset includes records such as:

- Insurance claims
- Policy information
- Customer risk grades
- Claim amounts
- Fraud indicators
- Premium information
- Coverage details
- Claim dates

The analysis focuses on identifying high-loss claim categories, customer risk behaviour, statistical insurance relationships, fraud patterns, and anomalous insurance activities.

---

## EDA Workflow

### 1. Load

Load the processed insurance dataset from:

```text
data/processed/processed-data.csv
```

The dataset is generated from the ETL pipeline.

---

### 2. Profile

Generate a statistical overview of the insurance dataset.

Checks include:

- Row and column counts
- Missing values
- Duplicate records
- Numeric summaries
- Categorical summaries

---

### 3. Claim Type Analysis

Analyse insurance losses across claim categories.

Analysis includes:

- Average claim amount by claim type
- Total losses by claim type
- Claim frequency analysis
- High-loss claim categories
- Claim severity ranking

---

### 4. Risk Grade Analysis

Analyse customer and policy risk behaviour.

Analysis includes:

- Average claim amount by risk grade
- Fraud rate by risk grade
- Risk score comparison
- High-risk customer profiling
- Premium comparison analysis

---

### 5. ANOVA Statistical Test

Test whether claim amounts differ significantly across insurance groups.

The project uses:

```python
scipy.stats.f_oneway()
```

ANOVA is used to determine whether mean claim amounts differ significantly between insurance categories.

---

### 6. Kruskal-Wallis Test

Run non-parametric statistical testing on insurance claim groups.

The project uses:

```python
scipy.stats.kruskal()
```

The Kruskal-Wallis test evaluates whether insurance groups differ significantly when data distributions are not normal.

---

### 7. Feature Importance Analysis

Analyse which insurance variables most strongly influence claim amounts.

The project computes:

- Pearson correlation
- Feature ranking
- Correlation strength
- Risk factor importance

Feature importance helps identify the variables driving insurance losses.

---

### 8. Forecasting

Forecast future insurance metrics using exponential smoothing.

The project uses:

```python
statsmodels.tsa.holtwinters.ExponentialSmoothing
```

Forecasting includes:

- Future claim amount estimation
- Trend analysis
- Time-series smoothing
- Next-period prediction

---

### 9. Fraud Pattern Analysis

Analyse fraudulent insurance behaviour.

Analysis includes:

- Fraud rate by claim type
- Fraud rate by customer risk grade
- Fraud comparison statistics
- Fraudulent vs legitimate claim profiling

The project also includes:

```python
flag_fraud_patterns()
```

---

### 10. Anomaly Detection

Detect statistically unusual insurance records using:

- IQR method
- Z-score method
- Fraud anomaly detection
- Insurance risk anomaly detection

Examples include:

- Extremely high claim amounts
- Unusual customer behaviour
- Abnormal premium values
- Suspicious fraud patterns

Transactions flagged by multiple methods are treated as confirmed anomalies.

---

## Input and Output

### Input

```text
data/processed/processed-data.csv
```

### Outputs

```text
reports/insurance_eda_report.html
reports/anomalies.csv
reports/figures/
notebooks/insurance_deep_dive.ipynb
```

---

## Project Structure

```text
P03-insurance-eda/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── insurance_deep_dive.ipynb
│
├── reports/
│   ├── insurance_eda_report.html
│   ├── anomalies.csv
│   └── figures/
│
├── sql/
│
├── src/
│   ├── data_extractor.py
│   ├── validator.py
│   ├── transformer.py
│   ├── insurance_eda_engine.py
│   ├── anomaly_detector.py
│   ├── html_reporter.py
│   └── query_runner.py
│
├── tests/
│   ├── test_insurance_eda.py
│   ├── test_anomaly_detector.py
│   └── test_html_reporter.py
│
├── run.py
├── config.py
├── requirements.txt
└── README.md
```

---

## Claim Type Analysis

The project analyses insurance losses by:

- Claim type
- Policy category
- Customer risk grade
- Fraud status
- Time period

Metrics generated include:

- Total claim losses
- Average claim severity
- Fraud percentages
- High-loss categories
- Claim ranking

---

## Risk Grade Analysis

The project evaluates customer risk behaviour across insurance categories.

Metrics generated include:

- Average claim amount
- Fraud rate
- Premium comparison
- Risk score comparison
- Total claim volume

The analysis helps identify high-risk insurance groups.

---

## ANOVA Statistical Test

The project evaluates whether insurance claim amounts differ significantly across insurance groups.

Variables analysed include:

- `claim_type`
- `risk_grade`
- `amount_claimed`

Decision rule:

- If `p < 0.05` → relationship is statistically significant
- If `p >= 0.05` → groups are statistically similar

---

## Kruskal-Wallis Test

The project evaluates non-parametric statistical differences between insurance groups.

The test is used when:

- Data is skewed
- Data is non-normal
- Insurance distributions contain outliers

Decision rule:

- If `p < 0.05` → statistically significant difference exists
- If `p >= 0.05` → no statistically significant difference

---

## Feature Importance Analysis

The project identifies which insurance variables most strongly influence claim outcomes.

Analysis includes:

- Correlation ranking
- Risk driver identification
- Premium influence analysis
- Fraud predictor analysis

---

## Forecasting

The project forecasts future insurance metrics using exponential smoothing.

Forecasting outputs include:

- Next-period claim estimate
- Trend direction
- Smoothed projections
- Future loss estimation

---

## Fraud Pattern Analysis

The project analyses fraudulent insurance behaviour by:

- Claim type
- Risk grade
- Premium category
- Customer profile
- Time period

Metrics generated include:

- Fraud counts
- Fraud percentages
- Fraud severity
- Fraud comparison statistics

---

## Anomaly Detection

The anomaly detection module identifies statistically unusual insurance activities.

Examples include:

- Extremely high claim amounts
- Suspicious fraud activity
- Abnormal risk behaviour
- Unusual premium values
- Fraudulent claims with statistically normal amounts

Detected anomalies are exported to:

```text
reports/anomalies.csv
```

---

## Visualisations

The notebook generates and saves insurance visualisations including:

- Claim amount distributions
- Risk grade comparisons
- Correlation heatmaps
- Forecast trend charts
- Fraud pattern visualisations
- Insurance anomaly scatter plots

Saved charts are stored in:

```text
reports/figures/
```

---

## HTML Reporting

The project generates a formatted HTML insurance report.

Generated file:

```text
reports/insurance_eda_report.html
```

The report includes:

- Dataset overview
- Statistical summaries
- Fraud analysis
- Forecasting outputs
- Anomaly summaries
- Visualisation results

---

## How to Run

Run the complete insurance EDA pipeline:

```bash
python run.py
```

The pipeline performs:

1. SQL extraction
2. Validation
3. Transformation
4. EDA analysis
5. Statistical testing
6. Forecasting
7. Fraud analysis
8. Anomaly detection
9. HTML report generation

---

## Tests

Run unit tests using:

```bash
pytest tests/
```

Tests cover:

- InsuranceEDAEngine methods
- ANOVA testing
- Kruskal-Wallis testing
- Forecasting
- Fraud pattern analysis
- Feature importance analysis
- Anomaly detection
- HTML reporting
- Data quality validation

---

## Git Workflow

```bash
git status
git add .
git commit -m "feat: complete production-grade insurance EDA pipeline"
git push
```

---

## Success Criteria Achieved

- InsuranceEDAEngine implemented
- ANOVA testing completed
- Kruskal-Wallis testing completed
- Feature importance analysis completed
- Forecasting implemented
- Fraud pattern analysis completed
- AnomalyDetector implemented
- HTMLReporter implemented
- HTML reports generated
- Visualisations generated
- Unit tests completed
- Project pushed to GitHub

---
 # #   I n s u r a n c e   E D A   B r a n c h   U p d a t e 
 A d d e d   p u l l   r e q u e s t   w o r k f l o w   u p d a t e .  
 