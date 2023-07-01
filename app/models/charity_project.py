from sqlalchemy import Column, String, Text

from app.services import constants as c
from app.models.base_charity import BaseCharity


class CharityProject(BaseCharity):
    """
    Модель благотворительных проектов.
    """
    name = Column(
        String(c.CHARITY_PROJECT_NAME_MAX),
        unique=True, nullable=False
    )
    description = Column(Text, nullable=False)
