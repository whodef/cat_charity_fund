from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description)

app.include_router(main_router)


@app.get('/')
def read_root() -> dict:
    """
    Корневой endpoint, который приветствует пользователя.

    ### Gets:
    Получает приветственное сообщение.

    ### Returns:
    Словарь, содержащий приветственное сообщение.

        dict: {"Hello, Human":"Let's go to the docs"}
    """
    return {'Hello, Human': 'Let\'s go to the docs'}
