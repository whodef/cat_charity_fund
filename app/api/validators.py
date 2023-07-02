import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate
from app.services import constants as c


async def check_name_duplicate(
        project_name: str, session: AsyncSession
) -> None:
    """
    Проверяется, доступно ли указанное имя проекта для использования.
    """
    if await charity_project_crud.get_object_id_by_name(
            project_name, CharityProject, session):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=c.PROJECT_NAME_ALREADY_EXISTS)


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession) -> CharityProject:
    """
    Проверяет, существует ли благотворительный проект с заданным ID.
    """
    charity_project = await charity_project_crud.get(project_id, session)
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=c.PROJECT_NOT_FOUND)
    return charity_project


async def check_charity_project_invested_no_money(
        project_id: int, session: AsyncSession) -> None:
    """
    Выполняет проверку, были ли произведены инвестиции в указанный проект.
    """
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=c.DELETION_NOT_ALLOWED)


async def check_charity_project_fully_invested(
        charity_project: CharityProject) -> None:
    """
    Функция выполняет проверку на то, был ли проект полностью проинвестирован.
    """
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=c.PATCH_NOT_ALLOWED)


async def check_new_full_amount(
        charity_project: CharityProject,
        obj_in: CharityProjectUpdate) -> CharityProject:
    """
    Функция проверяет, что новая сумма пожертвований для проекта не
    меньше уже внесенной суммы.

    Если новая целевая сумма уже достигнута, статус проекта меняется
    на fully_invested и присваивается close_date.
    """

    if charity_project.invested_amount > obj_in.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=c.INVALID_FULL_AMOUNT)

    if charity_project.invested_amount == obj_in.full_amount:
        charity_project.fully_invested = True
        charity_project.close_date = datetime.datetime.now()

    return charity_project
