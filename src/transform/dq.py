import json
import pandas as pd
import pandera as pa
from pandera import Column, Check

def run_checks(vacc: pd.DataFrame, severe: pd.DataFrame, pop: pd.DataFrame, out_path: str):
    Vacc = pa.DataFrameSchema({
        "area": Column(str, Check.str_length(min_value=1)),
        "coverage_1st": Column(float, Check.in_range(0, 100), nullable=True),
        "coverage_2nd": Column(float, Check.in_range(0, 100), nullable=True),
    }, coerce=True, strict=False)
    Sev = pa.DataFrameSchema({
        "month": Column(pa.DateTime, nullable=False),
        "area": Column(str, Check.str_length(min_value=1)),
        "age_group": Column(str, Check.str_length(min_value=1)),
        "severe_cases": Column(int, Check.ge(0)),
    }, coerce=True, strict=False)
    Pop = pa.DataFrameSchema({
        "area": Column(str, Check.str_length(min_value=1)),
        "age_group": Column(str, Check.str_length(min_value=1)),
        "population": Column(int, Check.ge(0)),
    }, coerce=True, strict=False)

    results = {}
    try:
        Vacc.validate(vacc, lazy=True)
        results["vacc_ok"] = True
    except pa.errors.SchemaErrors as e:
        results["vacc_ok"] = False
        results["vacc_errors"] = e.failure_cases.to_dict("records")

    try:
        Sev.validate(severe, lazy=True)
        results["severe_ok"] = True
    except pa.errors.SchemaErrors as e:
        results["severe_ok"] = False
        results["severe_errors"] = e.failure_cases.to_dict("records")

    try:
        Pop.validate(pop, lazy=True)
        results["pop_ok"] = True
    except pa.errors.SchemaErrors as e:
        results["pop_ok"] = False
        results["pop_errors"] = e.failure_cases.to_dict("records")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return results
