from pydantic import BaseModel
from fastapi_users.db import BaseUserDB
from fastapi_users.models import BaseUserCreate, BaseUserUpdate


class User(BaseModel):
    """
    Схема с базовыми полями модели пользователя (за исключением пароля).
    """
    pass


class UserDB(User, BaseUserDB):
    """
    Схема, описывающая модель User в БД."""
    pass


class UserCreate(BaseUserCreate):
    """
    Схема для регистрации пользователя;

    Обязательно должны быть переданы email и password.
    Любые другие поля, передаваемые в запросе будут проигнорированы.
    """
    pass


class UserUpdate(BaseUserUpdate):
    """
    Схема для обновления объекта пользователя.

    Содержит все базовые поля модели (в том числе и пароль).
    Все поля опциональны. Если запрос передаёт обычный пользователь
    (а не SuperUser), то поля is_active, is_superuser, is_verified исключаются.
    """
    pass
