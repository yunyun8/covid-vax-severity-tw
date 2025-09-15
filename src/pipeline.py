import argparse
import pandas as pd
import yaml
from pathlib import Path
from extract.vaccination_coverage import load_csv as load_vacc
from extract.cdc_severe import load_csv as load_severe
from extract.population import load_csv as load_pop
from transform.dq import run_checks
from transform.age_standardize import compute_age_standardized_rates

def main(date_str: str, config_path: str = "configs/config.yaml"):
    cfg = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))

    vacc_path = cfg["input_files"]["vaccination_coverage"]
    severe_path = cfg["input_files"]["severe_monthly"]
    pop_path = cfg["input_files"]["population"]

    vacc = load_vacc(vacc_path)
    severe = load_severe(severe_path)
    pop = load_pop(pop_path)

    dq_out = cfg["outputs"]["dq_report"]
    dq = run_checks(vacc, severe, pop, dq_out)
    print("[DQ] report:", dq)

    weights = cfg["national_weights"]
    std = compute_age_standardized_rates(severe, pop, weights)

    vacc_latest = vacc.sort_values("date").groupby("area", as_index=False).tail(1)[["area","coverage_1st","coverage_2nd"]]
    out = std.merge(vacc_latest, on="area", how="left")
    Path(cfg["outputs"]["std_rates"]).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(cfg["outputs"]["std_rates"], index=False, encoding="utf-8")

    wcfg = cfg["watchlist"]
    watch = out.copy()
    watch["low_coverage_flag"] = watch["coverage_1st"].fillna(0) < wcfg["coverage_pct_threshold"]
    watch["high_risk_flag"] = watch["std_rate_per_100k"].fillna(0) > wcfg["risk_rate_threshold"]
    watch = watch[(watch["low_coverage_flag"]) & (watch["high_risk_flag"])].sort_values("std_rate_per_100k", ascending=False)
    watch[["month","area","std_rate_per_100k","coverage_1st","severe_cases"]].to_csv(cfg["outputs"]["watchlist"], index=False, encoding="utf-8")
    print("Saved:", cfg["outputs"]["std_rates"], cfg["outputs"]["watchlist"], dq_out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", type=str, required=False, help="ISO date for run context", default=None)
    ap.add_argument("--config", type=str, default="configs/config.yaml")
    args = ap.parse_args()
    main(args.date, args.config)
