from pydantic import BaseSettings

class Settings(BaseSettings):
    timezone: str = "UTC"
    forecast_horizon_days: int = 30

settings = Settings()
