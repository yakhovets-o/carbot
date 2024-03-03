from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger

from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)

    cars: Mapped[bool] = mapped_column(default=False)
    truck_cars: Mapped[bool] = mapped_column(default=False)
    currency: Mapped[str] = mapped_column(default='Usd')
    price_min: Mapped[int] = mapped_column(default=0)
    price_max: Mapped[int]
    tracking_date: Mapped[str]

    __av: Mapped['Av'] = relationship(backref='user')
    __kufar: Mapped['Kufar'] = relationship(backref='user')


class Av(Base):
    __tablename__ = 'av'

    link: Mapped[str] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey('user.tg_id', onupdate='CASCADE'), nullable=False)

    brand: Mapped[str] = mapped_column(String(30))
    model: Mapped[str] = mapped_column(String(30))
    year: Mapped[str] = mapped_column(String(30))
    condition: Mapped[str] = mapped_column(String(30))
    engine_type: Mapped[str] = mapped_column(String(30))
    engine_capacity: Mapped[str] = mapped_column(String(30))

    region: Mapped[str] = mapped_column(String(60))
    city: Mapped[str] = mapped_column(String(60))

    price_br: Mapped[int]
    price_usd: Mapped[int]

    date_time_ad: Mapped[datetime]
    date_time_now: Mapped[datetime] = mapped_column(DateTime, default=func.now())


class Kufar(Base):
    __tablename__ = 'kufar'

    link: Mapped[str] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey('user.tg_id', onupdate='CASCADE'), nullable=False)

    brand: Mapped[str] = mapped_column(String(30))
    model: Mapped[str] = mapped_column(String(30))
    year: Mapped[str] = mapped_column(String(30))
    condition: Mapped[str] = mapped_column(String(30))
    engine_type: Mapped[str] = mapped_column(String(30))
    engine_capacity: Mapped[str] = mapped_column(String(30))

    region: Mapped[str] = mapped_column(String(60))
    city: Mapped[str] = mapped_column(String(60))

    price_br: Mapped[str] = mapped_column(String(30))
    price_usd: Mapped[str] = mapped_column(String(30))

    date_time_ad: Mapped[datetime]
    date_time_now: Mapped[datetime] = mapped_column(DateTime, default=func.now())
