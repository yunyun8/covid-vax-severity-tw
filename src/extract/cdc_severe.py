import pandas as pd

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    rename = {"county":"area","city":"area","cases_severe":"severe_cases"}
    df = df.rename(columns=rename)
    if "month" in df.columns:
        df["month"] = pd.to_datetime(df["month"], errors="coerce").dt.to_period("M").dt.to_timestamp()
    for col in ["severe_cases","deaths"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    for col in ["age_group","area"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df.dropna(subset=["area","age_group","month"])
