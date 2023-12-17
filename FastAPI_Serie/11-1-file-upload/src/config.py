import os

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

current_directory = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_directory, "..", ".env")


class Settings(BaseSettings):
    app_name: str

    model_config = SettingsConfigDict(env_file=env_file_path)

    db_host: str
    db_port: int
    db_user: str
    db_pass: SecretStr
    db_name: str

    secret_key: SecretStr
    algorithm: str
    access_token_expire_minutes: int

    redis_host: str
    redis_port: int

    smtp_user: str
    smtp_password: SecretStr


settings = Settings()
