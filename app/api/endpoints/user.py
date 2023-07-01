from http import HTTPStatus
from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, GetUser, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['Auth'])

router.include_router(
    fastapi_users.get_register_router(GetUser, UserCreate),
    prefix='/auth',
    tags=['Auth'])

router.include_router(
    fastapi_users.get_users_router(GetUser, UserUpdate),
    prefix='/users',
    tags=['Users'])


@router.delete(
    '/users/{id}',
    tags=['Users'],
    deprecated=True)
def delete_user(id: str):
    """
    **Не используйте удаление, деактивируйте пользователей.**
    """
    raise HTTPException(status_code=HTTPStatus.METHOD_NOT_ALLOWED)
