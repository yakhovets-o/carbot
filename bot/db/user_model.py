from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import DateTime
from sqlalchemy import func


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)

    cars: Mapped[bool] = mapped_column(default=False)
    truck_cars: Mapped[bool] = mapped_column(default=False)

    currency: Mapped[str] = mapped_column(default='Usd')

    price_min: Mapped[int] = mapped_column(default=0)
    price_max: Mapped[int]

    update_period_min: Mapped[int] = mapped_column(default=10)
    tracking_date: Mapped[str]


