from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FoodSnapApi"
    admin_email: str = "example@mail.com"
    host_url: str

    model_config = SettingsConfigDict(env_file=".env")