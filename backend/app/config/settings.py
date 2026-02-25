from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # DATABASE
    DATABASE_URL : str = "postgresql+asyncpg://cs6417:CS6417!UNB@localhost:5432/cs6417-rowing-shop"

    # SECRETS
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    
    # Token expiration time
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

def get_settings():
    return Settings()