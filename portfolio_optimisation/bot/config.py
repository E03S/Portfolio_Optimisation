import pathlib

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ROOT_PATH / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )
    bot_token: str = Field(
        default=str(ROOT_PATH / "models/titles_embedding_financial_data.cbm")
    )
    api_port: int = Field(default=8000)
    api_host: str = Field(default="http://localhost")


settings = Settings(_env_file_encoding="utf-8")
