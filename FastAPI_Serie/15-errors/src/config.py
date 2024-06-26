import os

from pydantic import SecretStr
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

    db_host_test: str | None = None
    db_port_test: int | None = None
    db_user_test: str | None = None
    db_pass_test: SecretStr | None = None
    db_name_test: str | None = None


settings = Settings()
