import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AppSettings(BaseSettings):
    access_token_expire_minutes: str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_minutes: str = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")
    algorithm: str = os.getenv("ALGORITHM")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    jwt_refresh_secret_key: str = os.getenv("JWT_REFRESH_SECRET_KEY")
    cache_expiration_seconds: str = os.getenv("CACHE_EXPIRATION_SECONDS")
    elasticsearch_url: str = os.getenv("ELASTICSEARCH_URL")
    elasticsearch_post_index: str = os.getenv("ELASTICSEARCH_POST_INDEX")
