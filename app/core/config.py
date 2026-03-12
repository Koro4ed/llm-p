from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    env: str

    jwt_secret: str
    jwt_alg: str
    access_token_expire_minutes: int

    sqlite_path: str

    openrouter_api_key: str
    openrouter_base_url: str
    openrouter_model: str
    openrouter_site_url: str
    openrouter_app_name: str

    class Config:
        env_file = ".env"


settings = Settings()
