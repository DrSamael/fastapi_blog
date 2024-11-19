from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    access_token_expire_minutes: str
    refresh_token_expire_minutes: str
    algorithm: str
    jwt_secret_key: str
    jwt_refresh_secret_key: str
