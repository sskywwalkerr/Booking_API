"""settings  and configs  for the project"""
import os
from envparse import Env
from pydantic_settings import BaseSettings, SettingsConfigDict

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/postgres"
)# connect string for the database
APP_PORT = env.int("APP_PORT", default=8000)


SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://postgres_test:postgres_test@127.0.0.1:5433/postgres_test"
)# connect string for the database


# class Settings(BaseSettings):
#     redis_host: str = os.environ.get("REDIS_HOST", "localhost")
#     redis_port: int = int(os.environ.get("REDIS_PORT", 6379))
#     redis_db: int = int(os.environ.get("REDIS_DB", 0))
#     # redis_password: str = os.environ.get("REDIS_PASSWORD")
#
#     model_config = SettingsConfigDict(env_file=".env")
#
# settings = Settings()
