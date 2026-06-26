import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-key-insegura")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    POKEAPI_BASE_URL: str = "https://pokeapi.co/api/v2"
    FIRST_GEN_LIMIT: int = 151

settings = Settings()