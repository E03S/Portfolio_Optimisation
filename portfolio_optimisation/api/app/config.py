import pathlib

from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent
APP_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ROOT_PATH / ".env"), env_file_encoding="utf-8", extra="ignore"
    )
    regressor_path: str = Field(
        default=str(APP_PATH / "models/financial_data_only.cbm")
    )
    preproccessor_path: str = Field(
        default=str(APP_PATH / "models/preprocessor_pipeline.pkl")
    )
    app_port: int = Field(default=8000)


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
