from fastapi import FastAPI
from app.api import main_router
from app.core.config import settings as s

app = FastAPI(
    title=s.app_title,
    description=s.description,
    version=s.version,
)

app.include_router(main_router)


@app.get('/')
def read_root() -> dict:
    """Корневой endpoint, который приветствует пользователя.

    ### Gets:
    Получает приветственное сообщение.

    ### Returns:
    Словарь, содержащий приветственное сообщение.

        dict: {"Hello, Human":"Let's go to the docs"}
    """
    return {'Hello, Human': 'Let\'s go to the docs'}
