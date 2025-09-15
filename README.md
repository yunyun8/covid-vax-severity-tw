# Taiwan COVID-19 Vaccination vs Severe/Death ETL (County × Age)

This project builds a reproducible pipeline that joins **vaccination coverage** and **COVID-19 severe/death cases** in Taiwan,
and outputs **(1) age-standardized severe rate by county**, **(2) coverage quantiles**, and **(3) a watchlist: high risk & low coverage**.

## Data Sources (official)
- Taiwan CDC — **COVID-19 Vaccination Statistics** (attachments with county coverage; updated e.g. 2025-09-08).  
  Page: https://www.cdc.gov.tw/Category/Page/9jFXNbCe-sFK9EImRRi2Og
- Taiwan CDC Open Data — **COVID-19 with Severe Complications** (by area/age/sex, monthly).  
  Portal search examples (choose the dataset matching your needs): https://data.cdc.gov.tw/
- Ministry of the Interior (MOI) — **Population by Age Groups, Counties/Cities** (for standardization weights).  
  Open Data: https://data.gov.tw/en/datasets/18315

> ⚠️ Not all coverage tables are published in machine-readable CSV every time. This repo includes **sample CSVs** and a clean interface so you can either
> 1) paste the latest county coverage CSV into `data/raw/vacc_coverage.csv`, or  
> 2) point to your own download function/URL via `configs/config.yaml`.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

# (A) Run with sample data (immediate)
python src/pipeline.py --date 2025-08-31

# (B) Run with your own CSVs
# Put CDC county coverage CSV at data/raw/vacc_coverage.csv (columns: date,area,coverage_1st,coverage_2nd)
# Put CDC severe monthly at data/raw/severe_monthly.csv   (columns: month,area,age_group,severe_cases,deaths)
# Put MOI population at data/raw/population.csv           (columns: area,age_group,population)
python src/pipeline.py --date 2025-08-31
```

Outputs are written to `outputs/`:
- `age_standardized_rates.csv`
- `county_watchlist.csv` (high risk & low coverage)
- `dq_report.json` (schema checks summary)

## Age Standardization (direct method)
We compute age-specific rates r_i = cases_i / pop_i for i in age groups: `0-17, 18-49, 50-64, 65-74, 75+` (editable in config),
then aggregate by county: **std_rate = Σ w_i * r_i**, where w_i are **national weights** (MOI national age shares).

## Project Layout
```
configs/
  config.yaml            # endpoints, age groups, thresholds
src/
  extract/
    vaccination_coverage.py  # load latest county coverage
    cdc_severe.py            # load monthly severe/deaths by area × age
    population.py            # load MOI population
  transform/
    cleaning.py
    age_standardize.py
    dq.py
  pipeline.py                # glue: extract → dq → transform → outputs
tests/
  sample_data/               # small CSVs to run immediately
.github/workflows/ci.yml     # CI + scheduled run (cron; uploads artifacts)
outputs/                     # results here (ignored by git)
data/raw/                    # drop-in CSVs (ignored by git)
```

## Run on Schedule (GitHub Actions)
- This repo includes `.github/workflows/ci.yml` that runs **daily at 06:00 Asia/Taipei** and on pushes.
- It **uploads artifacts** (outputs) for download from each run.

## Configuration
See `configs/config.yaml` for age bins, standardization weights source, and watchlist thresholds.

## Notes
- Use only **aggregate** public data. Do **not** commit any personally identifiable information (PHI) or microdata.
- For CDC PDFs, convert tables into CSV before loading (manual or semi-automated). Keep provenance notes in the README.
