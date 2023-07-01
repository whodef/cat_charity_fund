from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base_charity import BaseCharity


class Donation(BaseCharity):
    """
    Модель пожертвований.
    """
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'))
    comment = Column(Text, nullable=True)
