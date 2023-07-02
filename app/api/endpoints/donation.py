from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation, User
from app.schemas.donation import DonationCreate, DonationDB, UserDonationRead
from app.services.find_sources import find_sources
from app.services.invest import invest_money_into_project

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude={'close_date'})
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
) -> list[DonationDB]:
    """
    Получение списка пожертвований. Только для SuperUser.

    ### Args:

        session: объект сессии

    ### Returns:

        Список всех существующих пожертвований
    """
    all_donations = await donation_crud.get_multi(session)

    return all_donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={
        'user_id', 'fully_invested',
        'invested_amount', 'close_date'
    }
)
async def create_new_donation(
        new_donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> DonationDB:
    """
    Сделать пожертвование.

    ### Args:

        new_donation: новое пожертвование

        данные пользователя, сделавшего пожертвования

        session: объект сессии

    ### Returns:

        Только что созданное пожертвование.
    """
    new_donation = await donation_crud.create(new_donation, session, user)

    sources = await find_sources(session, CharityProject)

    # if sources:
    #     changed_sources = invest_money_into_project(
    #         target=new_donation, sources=sources)
    #     session.add(*changed_sources)

    if sources:
        changed_sources = invest_money_into_project(
            target=new_donation, sources=sources)
        if changed_sources:
            session.add_all(changed_sources)

    await session.commit()
    await session.refresh(new_donation)

    return new_donation


@router.get('/my', response_model=list[UserDonationRead])
async def get_my_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> list[UserDonationRead]:
    """
    Получает список пожертвований пользователя.

    ### Args:

        user: Данные пользователя, который делает запрос

        session: объект сессии

    ### Returns:

        Список пожертвований пользователя
    """
    user_donations = await donation_crud.get_users_objects(
        user.id, Donation, session)

    return user_donations
