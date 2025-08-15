import numpy as np

def smape(y_true, y_pred) -> float:
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    denom = (np.abs(y_true) + np.abs(y_pred)) / 2.0
    denom[denom == 0] = 1.0
    return float(np.mean(np.abs(y_true - y_pred) / denom)) * 100
