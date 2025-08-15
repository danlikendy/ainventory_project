import math

def safety_stock(z: float, demand_std: float, lead_time_days: float) -> float:
    return z * demand_std * math.sqrt(lead_time_days)
