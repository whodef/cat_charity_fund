from fastapi import APIRouter
from app.api import charity_project, donation, user

main_router = APIRouter()


# User
main_router.include_router(
    router=user.router
)

# Charity
main_router.include_router(
    router=charity_project.router,
    prefix='/charity_project',
    tags=['Charity Projects'],
)

# Donation
main_router.include_router(
    router=donation.router,
    prefix='/donation',
    tags=['Donations']
)
