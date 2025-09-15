import pandas as pd
from dateutil.parser import parse

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    rename = {
        "county": "area",
        "city": "area",
        "first_dose": "coverage_1st",
        "second_dose": "coverage_2nd"
    }
    df = df.rename(columns=rename)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["coverage_1st","coverage_2nd"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "area" in df.columns:
        df["area"] = df["area"].astype(str).str.strip()
    return df.dropna(subset=["area"])
