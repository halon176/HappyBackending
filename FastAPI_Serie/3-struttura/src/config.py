import os

from pydantic_settings import BaseSettings, SettingsConfigDict

current_directory = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_directory, "..", ".env")


class Settings(BaseSettings):
    app_name: str

    model_config = SettingsConfigDict(env_file=env_file_path)


settings = Settings()
