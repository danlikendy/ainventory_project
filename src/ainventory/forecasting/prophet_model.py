from prophet import Prophet
import pandas as pd

def fit_prophet(df: pd.DataFrame, ds_col: str, y_col: str) -> Prophet:
    m = Prophet()
    m.fit(df.rename(columns={ds_col: "ds", y_col: "y"}))
    return m
