import pandas as pd

def compute_age_standardized_rates(severe_df: pd.DataFrame, pop_df: pd.DataFrame, weights: dict) -> pd.DataFrame:
    df = severe_df.merge(pop_df, on=["area","age_group"], how="left")
    df["rate_per_100k"] = (df["severe_cases"] / df["population"].replace({0: pd.NA})) * 100000
    df["w"] = df["age_group"].map(weights).astype(float)
    df = df.dropna(subset=["rate_per_100k","w"])
    grouped = df.groupby(["month","area"], as_index=False).apply(
        lambda g: pd.Series({
            "std_rate_per_100k": (g["rate_per_100k"] * g["w"]).sum(),
            "severe_cases": g["severe_cases"].sum()
        })
    ).reset_index(drop=True)
    return grouped
