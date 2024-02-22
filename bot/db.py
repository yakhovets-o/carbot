

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy import DATETIME
from sqlalchemy import func
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class ParametersAd:
    brand: Mapped[str] = mapped_column(String(255))
    model: Mapped[str] = mapped_column(String(255))
    year: Mapped[str] = mapped_column(String(255))
    engine_type: Mapped[str] = mapped_column(String(255))
    engine_capacity: Mapped[str] = mapped_column(String(255))

    region: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))

    price_br: Mapped[int] = mapped_column(default=0)
    price_usd: Mapped[int] = mapped_column(default=0)

    link: Mapped[str] = mapped_column(String(255), primary_key=True)

    date_time_post: Mapped[DATETIME]
    date_time_now: Mapped[DATETIME] = mapped_column(default=func.now())


class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    cars: Mapped[bool] = mapped_column(default=False)
    truck_cars: Mapped[bool] = mapped_column(default=False)
    price_min: Mapped[int] = mapped_column(default=0)
    price_max: Mapped[int] = mapped_column(default=1_000)
    update_period_min: Mapped[int] = mapped_column(default=10)
    tracking_time: Mapped[DATETIME] = mapped_column(default=func.now)

    av: Mapped[list['Av']] = relationship(back_populates='user', cascade='all, delete-orphan')
    kufar: Mapped[list['Kufar']] = relationship(back_populates='user', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"{self.__class__.__name__!r}(user_id={self.user_id!r}, cars={self.cars!r}, truck_cars={self.truck_cars!r}," \
               f"price_min={self.price_min!r}, price_max={self.price_max!r}, update_period_min={self.update_period_min!r}," \
               f"tracking_time={self.tracking_time!r})"


class Kufar(Base, ParametersAd):
    __tablename__ = 'kufar'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user: Mapped['User'] = relationship(back_populates='kufar')

    def __repr__(self):
        return f"{self.__class__.__name__!r}(user_id={self.user_id}, brand={self.brand}," \
               f"model={self.model}, year={self.year}, engine_type={self.engine_type}," \
               f"engine_capacity={self.engine_capacity}, region={self.region}," \
               f"city={self.city}, price_br={self.price_br}, price_usd={self.price_usd}," \
               f"link={self.link}, date_time_post={self.date_time_post}, date_time_now={self.date_time_now}"


class Av(Base, ParametersAd):
    __tablename__ = 'av'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user: Mapped['User'] = relationship(back_populates='av')

    cond: Mapped[str] = mapped_column(String(255))

    def __repr__(self):
        return f"{self.__class__.__name__!r}(user_id={self.user_id}, brand={self.brand}," \
               f"model={self.model}, year={self.year}, engine_type={self.engine_type}," \
               f"engine_capacity={self.engine_capacity}, cond={self.cond}, region={self.region}," \
               f"city={self.city}, price_br={self.price_br}, price_usd={self.price_usd}," \
               f"link={self.link}, date_time_post={self.date_time_post}, date_time_now={self.date_time_now}"


engine = create_engine('sqlite+aiosqlite:///examplel.sqlite3', echo=True)

Base.metadata.create_all(engine)


