from typing import Union

import fastapi
import fastapi_users as fa_users
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
import fastapi_users.authentication as auth

from app import models, schemas
from app.core import config, db
from app.services import constants as c


async def get_user_db(
    session: db.AsyncSession = fastapi.Depends(db.get_async_session)
):
    """
    Подключения таблицы `user` в БД.

    ### Args:
     Объект сессии с БД.

        session (db.AsyncSession, optional):
            Defaults to fa.Depends(db.get_async_session)

    ### Yields:
    При обращении создаёт новое подключение к таблице `user` в БД.
    """
    yield SQLAlchemyUserDatabase(schemas.UserDB, session, models.UserTable)


def get_jwt_strategy() -> auth.JWTStrategy:
    """
    Получает настройки использования `JWT`.

    ### Returns:
    Объект с настройками `JWT`.

        auth.JWTStrategy
    """
    return auth.JWTStrategy(
        secret=config.settings.secret,
        lifetime_seconds=c.JWT_LIFE_TIME
    )


bearer_transport = auth.BearerTransport(tokenUrl='auth/jwt/login')

auth_backend = auth.AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(
    fa_users.BaseUserManager[schemas.UserCreate, schemas.UserDB]
):
    """
    Управление и проверки различных действий пользователя.

    ### Attrs:
    Схема обрабатываемых данных.

        user_db_model

    Ключ для кодирования токена сброса пароля.

        reset_password_token_secret

    Ключ кодирования токена проверки.

        verification_token_secret
    """
    user_db_model = schemas.UserDB
    reset_password_token_secret = config.settings.secret
    verification_token_secret = config.settings.secret

    async def validate_password(
        self,
        password: str,
        user: Union[schemas.UserCreate, schemas.UserDB],
    ) -> None:
        """
        Проверяет пароль пользователя.

        ### Args:
        Введённый пароль.

            password (str)

        Схема данных.

            user Union[schemas.UserCreate, schemas.UserDB]

        ### Raises:
        Слишком короткий пароль.

            fastapi_users.InvalidPasswordException

        Пароль содержит e-mail пользователя.

            fastapi_users.InvalidPasswordException

        """
        if len(password) < 3:
            raise fa_users.InvalidPasswordException(
                reason=c.ERR_LEN_PASSWORD
            )
        if user.email in password:
            raise fa_users.InvalidPasswordException(
                reason=c.ERR_EMAIL_IN_PASSWORD
            )

    async def on_after_register(
            self,
            user: schemas.UserDB,
            request: Union[None, fastapi.Request] = None
    ):
        """
        После регистрации пользователя.

        ### Args:
        Схема данных пользователя.

            user (schemas.UserDB)

        Объект запроса.

            request (Union[None, fastapi.Request]):
                Default is None
        """
        print(c.USER_IS_SIGNED)


async def get_user_manager(user_db=fastapi.Depends(get_user_db)):
    """
    Генератор объектов `UserManager`.

    ### Args:
    Подключение к таблице `user` в БД.

        user_db (_type_, optional):
            Defaults to fastapi.Depends(get_user_db)

    ### Yields:
    При обращении создаёт новый объект управления пользователями.
    """
    yield UserManager(user_db)

fastapi_users = fa_users.FastAPIUsers(
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
    user_model=schemas.User,
    user_create_model=schemas.UserCreate,
    user_update_model=schemas.UserUpdate,
    user_db_model=schemas.UserDB
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
