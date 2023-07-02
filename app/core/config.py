from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    app_title: str = 'QRKot'
    app_description: str = 'API проекта QRKot'
    database_url: str = 'sqlite+aiosqlite:///./qrkot.db'
    secret: str = 'AAA-DEADLINE-SOON-AAA'

    class Config:
        env_file = '.env'


settings = Settings()
