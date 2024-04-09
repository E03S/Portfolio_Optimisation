import pathlib

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent.parent
APP_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ROOT_PATH / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )
    regressor_path: str = Field(
        default=str(APP_PATH / "models/titles_embedding_financial_data.cbm")
    )
    preproccessor_path: str = Field(
        default=str(APP_PATH / "models/pipeline_news_embeddings.pkl")
    )
    app_port: int = Field(default=8000)
    benzinga_token: str = Field(default="")


settings = Settings(_env_file_encoding="utf-8")

print(settings.benzinga_token)