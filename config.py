from pydantic import field_validator
from functools import lru_cache

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    base_url: str = "https://api.nal.usda.gov/fdc/v1"

    jwt_key: str
    jwt_algo: str = "HS256"
    jwt_expiry_time: int = 30
    
    mongodb_database_name: str = "calorie_counter"
    mongo_url: str = "mongodb://localhost:27017"

    rate_limit_window_minutes: int = 1
    rate_limit_requests: int = 15
    
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    environment: str = "localhost"
    version_prefix: str = "/v1"

    @field_validator('jwt_key')
    def validate_jwt_key(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("JWT Key should be 32 chars long!")
        return v

    @field_validator('api_key')
    def validate_api_key(cls, v: str):
        if not v:
            raise ValueError('USDA API Key is mandatory!!')
        return v
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = Settings()