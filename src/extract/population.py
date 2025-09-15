import pandas as pd

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    rename = {"county":"area","city":"area","pop":"population","people":"population"}
    df = df.rename(columns=rename)
    df["area"] = df["area"].astype(str).str.strip()
    df["age_group"] = df["age_group"].astype(str).str.strip()
    df["population"] = pd.to_numeric(df["population"], errors="coerce").fillna(0).astype(int)
    return df
