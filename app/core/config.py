from typing import Union

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    path: str
    echo: Union[None, bool] = None
    app_title: str = 'QRKot'
    description: str = 'API проекта QRKot.'
    version: str = '1.0.8'
    database_url: str = 'sqlite+aiosqlite:///./development.db'
    debug: bool = False
    secret: str = 'A-l0ng-st0ry-sh0rt'

    # Google API
    type: Union[None, str] = None
    project_id: Union[None, str] = None
    private_key_id: Union[None, str] = None
    private_key: Union[None, str] = None
    auth_uri: Union[None, str] = None
    token_uri: Union[None, str] = None
    auth_provider_x509_cert_url: Union[None, str] = None
    client_x509_cert_url: Union[None, str] = None
    client_email: Union[None, str] = None
    client_id: Union[None, str] = None
    email: Union[None, str] = None

    # # Start Superuser auto_create
    # first_superuser_email: Union[None, EmailStr] = None
    # first_superuser_password: Union[None, str] = None

    class Config:
        env_file = '.env'


settings = Settings()
