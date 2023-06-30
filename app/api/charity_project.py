from fastapi import APIRouter, Depends
from pydantic import PositiveInt
from app import schemas
from app.api import validators
from app.core import db, user
from app.crud import charity_projects_crud as ch_pr_crud
from app.crud import donation_crud as dn_crud
from app.services import constants as const
from app.services import utils

router = APIRouter()


@router.get(
    path='/',
    summary=const.GET_ALL_CHARITY_PROJECTS,
    response_model=list[schemas.CharityProjectResponse]
)
async def get_all_charity_projects(
    session: db.AsyncSession = Depends(db.get_async_session)
) -> list[schemas.CharityProjectResponse]:
    """
    ### Gets:
    Получает список всех благотворительных проектов.

    ### Args:
    Объект сессии с БД.

        session (db.AsyncSession, optional):
            Defaults to Depends(db.get_async_session)

    ### Returns:
    Список всех благотворительных проектов.

        List[schemas.CharityProjectResponse]
    """
    return await ch_pr_crud.get_all(
        session=session
    )


@router.post(
    path='/',
    summary=const.CREATE_CHARITY_PROJECTS,
    response_model=schemas.CharityProjectResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(user.current_superuser)]
)
async def create_charity_project(
    new_project: schemas.CharityProjectCreate,
    session: db.AsyncSession = Depends(db.get_async_session)
) -> schemas.CharityProjectResponse:
    """
    **Только для SuperUser.**

    ### Posts:
    Создает новый благотворительный проект.

    ### Args:
    Данные для создания нового благотворительного проекта.

        new_project (Schemas.CharityProjectCreateS

    Объект сессии с БД.

        session (db.AsyncSession, optional):
            Defaults to Depends(db.get_async_session)

    ### Returns:
    Новый созданный благотворительный проект.

        schemas.CharityProjectResponse
    """
    await validators.project_name_is_busy(
        name=new_project.name,
        session=session
    )

    project = await ch_pr_crud.create(
        new_obj=new_project,
        session=session
    )

    await utils.distribution_of_amounts(
        undivided=project,
        crud_class=dn_crud,
        session=session
    )

    return project


@router.delete(
    path='/{project_id}',
    summary=const.DELETE_CHARITY_PROJECTS,
    response_model=schemas.CharityProjectResponse,
    dependencies=[Depends(user.current_superuser)]
)
async def delete_charity_project(
    project_id: PositiveInt,
    session: db.AsyncSession = Depends(db.get_async_session)
) -> schemas.CharityProjectResponse:
    """
    **Только для SuperUser.**
    Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только **закрыть**.

    ### Delete:
    Закрывает благотворительный проект.

    ### Args:
    `id` удаляемого благотворительно проекта.

        project_id (int)

    Объект сессии с БД.

        session (db.AsyncSession, optional):
            Defaults to Depends(db.get_async_session)

    ### Returns:
    Закрытый благотворительный проект.

        schemas.CharityProjectResponse
    """
    project = await validators.has_investition(
        project_id=project_id,
        session=session
    )

    return await ch_pr_crud.remove(
        obj=project,
        session=session
    )


@router.patch(
    path='/{project_id}',
    summary=const.UPDATE_CHARITY_PROJECT,
    response_model=schemas.CharityProjectResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(user.current_superuser)]
)
async def update_charity_project(
    project_id: PositiveInt,
    update_data: schemas.CharityProjectUpdate,
    session: db.AsyncSession = Depends(db.get_async_session)
) -> schemas.CharityProjectResponse:
    """
    **Только для SuperUser.**
    Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной.

    ### Patch:
    Обновляет существующий благотворительный проект.

    ### Args:
    `id` редактируемого благотворительного проекта.

        project_id (int)

    Данные для обновления.

        update_data (schemas.CharityProjectUpdate)

    Объект сессии с БД.

        session (db.AsyncSession, optional):
            Defaults to Depends(db.get_async_session)

    ### Returns:
    Обновлённый благотворительный проект.

        schemas.CharityProjectResponse
    """
    project = await validators.allow_update_project(
        project_id=project_id,
        session=session,
        update_data=update_data
    )

    project = await ch_pr_crud.update(
        obj=project,
        session=session,
        update_data=update_data
    )
    await utils.distribution_of_amounts(
        undivided=project,
        crud_class=dn_crud,
        session=session
    )
    return project
