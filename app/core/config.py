from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:////app/data/app.db"
    SECRET_KEY: str = "your-secret-key"

    class Config:
        env_file = ".env"

settings = Settings()