from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    FREE_DATA_LIMIT: float = 1.0  # in km²
    EXTRA_DATA_COST: float = 2.0  # cost per square meter

    class Config:
        env_file = ".env"

settings = Settings()