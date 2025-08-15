import pandas as pd

def add_time_features(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    d = df.copy()
    dt = pd.to_datetime(d[date_col])
    d["dow"] = dt.dt.dayofweek
    d["month"] = dt.dt.month
    return d
