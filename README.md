# Data Modelling Kelompok 7

A Data Modelling course project focused on exploratory descriptive analysis and dashboard development using a teen social media and mental health indicators dataset.

The project uses Excel for the required course workflow and Python for reproducible data inspection, cleaning, profiling, and visualization preparation.

## Project Overview

This repository contains the working files for the Data Modelling group project. The current analytical direction is:

> Exploratory descriptive analysis of teen social media behavior, lifestyle factors, academic performance, and mental strain indicators.

The project does **not** attempt to diagnose mental health conditions or make causal claims. Any variables such as `depression_label`, `stress_level`, `anxiety_level`, and `addiction_level` are treated as dataset indicators for descriptive analysis only.

## Current Dataset Focus

The dataset includes variables such as:

- Age and gender
- Daily social media usage hours
- Platform usage
- Sleep hours
- Screen time before sleep
- Academic performance
- Physical activity
- Social interaction level
- Stress level
- Anxiety level
- Addiction level
- Depression indicator label

## Analytical Workflow

The current workflow is structured as follows:

1. Load the `.xlsx` dataset into Python.
2. Inspect dataset structure with `df.info()`.
3. Check missing values with `df.isnull().sum()`.
4. Remove empty or redundant columns.
5. Inspect categorical values using `value_counts()`.
6. Profile column variability using `nunique()`.
7. Generate descriptive statistics with `df.describe()`.
8. Create dashboard-friendly derived variables, such as:
   - `social_media_usage_group`
   - `mental_strain_score`
9. Compare descriptive patterns across groups.
10. Prepare visualizations for dashboard storytelling.

## Cleaning Decisions So Far

The initial inspection found several non-useful columns:

- `Unnamed: 13`
- `Unnamed: 14`
- `Daily Social Media`
- `StressLevel`

Cleaning rationale:

- `Unnamed: 13` and `Unnamed: 14` were empty Excel export artifacts.
- `Daily Social Media` duplicated `daily_social_media_hours`.
- `StressLevel` duplicated `stress_level`.

These columns were removed to avoid redundancy and confusion during analysis.

## Feature Engineering

Two derived variables are currently planned/used:

### Social Media Usage Group

Daily social media hours are grouped into three categories:

- `Low`: less than 3 hours/day
- `Moderate`: 3 to less than 6 hours/day
- `High`: 6 or more hours/day

### Mental Strain Score

A simple composite descriptive indicator calculated as the average of:

- `stress_level`
- `anxiety_level`
- `addiction_level`

This is used only as an exploratory summary measure, not as a clinical score.

## Tools

Primary course tool:

- Microsoft Excel

Python environment:

- Python
- pandas
- numpy
- openpyxl
- plotly
- matplotlib
- streamlit
- jupyter / ipykernel

## Setup

Create and activate a virtual environment.

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Sanity check:

```bash
python -c "import pandas, numpy, openpyxl, plotly, streamlit, matplotlib; print('all good')"
```

## Suggested Project Structure

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── outputs/
├── scripts/
├── requirements.txt
└── README.md
```

## Important Notes

- Avoid committing local virtual environments such as `.venv/`.
- Avoid using `pip freeze > requirements.txt` unless the environment is intentionally curated.
- Keep `requirements.txt` minimal and platform-independent.
- The project should remain descriptive and exploratory unless the assignment later explicitly asks for predictive modelling.

## Current Analytical Direction

Initial grouping by social media usage level showed that average wellbeing indicators were relatively similar across low, moderate, and high usage groups. Because of this, the next analysis should investigate whether stronger descriptive patterns appear across:

- Platform usage
- Screen time before sleep
- Social interaction level
- Numeric correlations between lifestyle and wellbeing indicators

## Status

Work in progress for Data Modelling course project.
