from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import validators as api_valid
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas import charity_project as cp
from app.services.find_sources import find_sources
from app.services.invest import invest_money_into_project

router = APIRouter()


@router.get(
    '/',
    response_model=list[cp.CharityProjectDB],
    response_model_exclude={'close_date'})
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
) -> list[cp.CharityProjectDB]:
    """
    Получение списка всех благотворительных проектов.

    ### Args:

        session: объект сессии

    ### Returns:

        Список проектов
    """
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=cp.CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: cp.CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
) -> cp.CharityProjectDB:
    """
    Создает новый благотворительный проект. Доступно только для SuperUser.

    ### Args:

        charity_project: Данные для создания проекта

        session: объект сессии

    ### Returns:

        Новый благотворительный проект
    """
    await api_valid.check_name_duplicate(charity_project.name, session)

    new_project = await charity_project_crud.create(charity_project, session)

    sources = await find_sources(session, Donation)
    if sources:
        changed_sources = invest_money_into_project(
            target=new_project, sources=sources
        )

        if changed_sources:
            session.add_all(changed_sources)

    return new_project


@router.patch(
    '/{charity_project_id}',
    response_model=cp.CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: cp.CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
) -> cp.CharityProjectDB:
    """
    Редактирует существующий благотворительный проект.

    Закрытый проект нельзя редактировать, так же
    нельзя установить сумму меньше, которая была вложена ранее.
    Доступно только для SuperUser.

    ### Args:

        charity_project_id: идентификатор редактируемого проекта

        obj_in: pydantic схема с данными для обновления

        session: объект сессии

    ### Returns:

        Обновленный благотворительный проект
    """
    charity_project = await api_valid.check_charity_project_exists(
        charity_project_id, session)

    await api_valid.check_charity_project_fully_invested(charity_project)

    if obj_in.name:
        await api_valid.check_name_duplicate(obj_in.name, session)

    if obj_in.full_amount and charity_project.invested_amount:
        charity_project = await api_valid.check_new_full_amount(
            charity_project, obj_in
        )

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=cp.CharityProjectDB,
    dependencies=[Depends(current_superuser)])
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> cp.CharityProjectDB:
    """
    Удаляет существующий благотворительный проект.

    Закрытый проект нельзя редактировать, так же
    нельзя установить сумму меньше, которая была вложена ранее.
    Доступно только для SuperUser.

    ### Args:

        charity_project_id: идентификатор проекта

        session: объект сессии

    ### Returns:

        Удаленный благотворительный проект
    """
    charity_project = await api_valid.check_charity_project_exists(
        charity_project_id, session
    )
    await api_valid.check_charity_project_invested_no_money(
        charity_project_id, session
    )
    await api_valid.check_charity_project_fully_invested(
        charity_project
    )
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )

    return charity_project
