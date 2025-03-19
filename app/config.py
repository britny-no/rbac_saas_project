from pydantic import BaseSettings

class Settings(BaseSettings):
    sqlalchemy_database_url: str

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expire_minutes: int
    
    cookie_key: str
    cookie_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()