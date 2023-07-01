import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base
from app.services import constants as c


class BaseCharity(Base):
    """
    Базовая модель благотворительных проектов и пожертвований.
    """
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount <= full_amount')
    )
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=c.DEFAULT_INVESTED_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.datetime.now)
    close_date = Column(DateTime)
