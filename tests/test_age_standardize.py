from transform.age_standardize import compute_age_standardized_rates
import pandas as pd

def test_age_standardized_rates():
    severe = pd.DataFrame({
        "month": pd.to_datetime(["2025-08-01","2025-08-01","2025-08-01","2025-08-01","2025-08-01"]*2),
        "area": ["Taipei City"]*5 + ["Kaohsiung City"]*5,
        "age_group": ["0-17","18-49","50-64","65-74","75+"]*2,
        "severe_cases": [1,5,8,10,12, 0,3,5,8,9]
    })
    pop = pd.DataFrame({
        "area": ["Taipei City"]*5 + ["Kaohsiung City"]*5,
        "age_group": ["0-17","18-49","50-64","65-74","75+"]*2,
        "population": [400000,1200000,500000,300000,200000, 350000,1100000,480000,280000,180000]
    })
    weights = {"0-17":0.15,"18-49":0.45,"50-64":0.2,"65-74":0.1,"75+":0.1}
    out = compute_age_standardized_rates(severe, pop, weights)
    assert set(out.columns) >= {"month","area","std_rate_per_100k","severe_cases"}
    assert len(out) == 2
