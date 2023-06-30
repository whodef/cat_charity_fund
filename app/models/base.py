from datetime import datetime
import sqlalchemy as sa


class GenericFields:
    """
    Общие поля для моделей.

    ### Attrs:
    Default's False.

        fully_invested (bool)

    Больше 0.

        full_amount (int)

    Default to 0.

        invested_amount (int)


    Дата создания. Default's `datetime.now()`

        create_date (datetime)

    Дата закрытия.

        close_date (datetime)
    """

    __table_args__ = (
        sa.CheckConstraint(
            'full_amount > 0', name='full_amount is not positive'
        ),
        sa.CheckConstraint(
            'invested_amount >= 0', name='invested_amount is negative'
        ),
        sa.CheckConstraint(
            'invested_amount <= full_amount',
            name='invested_amount is more than full_amount'
        ),
    )

    full_amount = sa.Column(sa.Integer, nullable=False)

    invested_amount = sa.Column(sa.Integer, nullable=False, default=0)

    fully_invested = sa.Column(
        sa.Boolean, nullable=False, default=False, index=True
    )

    create_date = sa.Column(sa.DateTime, nullable=False, default=datetime.now)

    close_date = sa.Column(sa.DateTime, nullable=True)
