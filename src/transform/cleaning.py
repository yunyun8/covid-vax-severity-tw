import pandas as pd

def align_age_bins(df: pd.DataFrame, age_map: dict) -> pd.DataFrame:
    if "age_group" not in df.columns:
        return df
    df = df.copy()
    df["age_group"] = df["age_group"].map(lambda x: age_map.get(x, x))
    return df

def normalize_area_names(df: pd.DataFrame, area_map: dict) -> pd.DataFrame:
    if "area" not in df.columns:
        return df
    df = df.copy()
    df["area"] = df["area"].map(lambda x: area_map.get(x, x))
    return df
