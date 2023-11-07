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


settings = Settings()
