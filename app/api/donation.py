from fastapi import APIRouter, Depends

from app import schemas
from app.core import user, db
from app.services import utils
from app.crud import charity_projects_crud
from app.crud import donation_crud as dc
from app.services import constants as c

router = APIRouter()


@router.get(
    path='/',
    summary=c.GET_ALL_DONATIONS,
    response_model=list[schemas.DonationLongResponse],
    dependencies=[Depends(user.current_superuser)]
)
async def get_all_donations(
    session: db.AsyncSession = Depends(db.get_async_session)
) -> list[schemas.DonationLongResponse]:
    """
    **Только для SuperUser.**

    ### Gets:
    Получает список всех пожертвований.

    ### Args:
    Объект сессии с БД.

        session (db.AsyncSession, optional):
            Defaults to Depends(db.get_async_session)

    ### Returns:
    Список всех пожертвований.

        List[schemas.DonationListResponse]
    """
    return await dc.get_all(session=session)


@router.post(
    path='/',
    summary=c.CREATE_DONATION,
    response_model=schemas.DonationShortResponse,
    response_model_exclude_none=True
)
async def create_donation(
    new_donation: schemas.DonationCreate,
    session: db.AsyncSession = Depends(db.get_async_session),
    user: schemas.UserDB = Depends(user.current_user)
) -> schemas.DonationShortResponse:
    """
    ### Posts:
    Записывает новое пожертвование.

    ### Args:
    Данные для записи нового пожертвования.

        new_donation (schemas.DonationCreate)

    Объект сессии с БД.

        session (db.AsyncSession, optional):
            Defaults to Depends(db.get_async_session)

    Данные пользователя, сделавшего пожертвование.

        user (schemas.UserDB, optional):
            Defaults to Depends(user.current_user)

    ### Returns:
    Новое учтённое пожертвование.

        schemas.DonationShortResponse
    """
    donation = await dc.create(
        new_obj=new_donation,
        session=session,
        user=user
    )
    await utils.distribution_of_amounts(
        undivided=donation,
        crud_class=charity_projects_crud,
        session=session
    )

    return donation


@router.get(
    path='/my',
    summary=c.GET_MY_DONATIONS,
    response_model=list[schemas.DonationShortResponse]
)
async def get_user_donations(
    user: schemas.UserDB = Depends(user.current_user),
    session: db.AsyncSession = Depends(db.get_async_session)
) -> list[schemas.DonationShortResponse]:
    """
    ### Gets:
    Получает список пожертвований пользователя.

    ### Args:
    Данные запрашивающего пользователя.

        user (schemas.UserDB, optional):
            Defaults to Depends(user.current_user)

    Объект сессии с БД.

        session (db.AsyncSession, optional):
            Defaults to Depends(db.get_async_session)

    ### Returns:
    Список всех пожертвований пользователя.

        List[schemas.DonationShortResponse]
    """
    return await dc.get_my_donations(
        user_id=user.id,
        session=session
    )
