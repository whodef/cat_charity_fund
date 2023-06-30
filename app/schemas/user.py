from fastapi_users import models


class User(models.BaseUser):
    """
    Схема с базовыми полями модели пользователя (за исключением пароля).
    """
    pass


class UserCreate(models.BaseUserCreate):
    """
    Схема для регистрации пользователя;

    Обязательно должны быть переданы email и password.
    Любые другие поля, передаваемые в запросе будут проигнорированы.
    """
    pass


class UserUpdate(models.BaseUserUpdate):
    """
    Схема для обновления объекта пользователя.

    Содержит все базовые поля модели (в том числе и пароль).
    Все поля опциональны. Если запрос передаёт обычный пользователь
    (а не SuperUser), то поля is_active, is_superuser, is_verified исключаются.
    """
    pass


class UserDB(User, models.BaseUserDB):
    """
    Схема, описывающая модель User в БД."""
    pass
