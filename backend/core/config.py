import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "CustomerInsight API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-customer-insight-2026-change-in-prod")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./customer_insight.db")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

settings = Settings()
