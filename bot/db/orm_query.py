from datetime import datetime

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.engine import session_maker
from bot.db.models import Av, Kufar, User


class OrmQuery:
    @staticmethod
    async def add_or_update_params(session: AsyncSession, data: dict) -> None:
        params = User(
            tg_id=data["user_id"],
            cars=data.get("cars", False),
            truck_cars=data.get("truck_cars", False),
            currency=data["currency"],
            price_min=data["price_min"],
            price_max=data["price_max"],
            tracking_date=data["tracking_date"],
        )
        await session.merge(params)
        await session.commit()

    @staticmethod
    async def add_kufar_ads(data: dict) -> None:
        async with session_maker() as session:
            params = Kufar(
                link=data["link"],
                tg_id=data["tg_id"],
                brand=data["Марка"],
                model=data["Модель"],
                year=data["Год"],
                condition=data["Состояние"],
                engine_type=data["Тип двигателя"],
                engine_capacity=data["Объем, л"],
                region=data["Область"],
                city=data["Город / Район"],
                price_br=data["price_br"],
                price_usd=data["price_usd"],
                date_time_ad=data["date_time_ad"],
            )
            session.add(params)
            await session.commit()

    @staticmethod
    async def add_av_ads(data: dict) -> None:
        async with session_maker() as session:
            params = Av(
                link=data["link"],
                tg_id=data["tg_id"],
                brand=data["brand"],
                model=data["model"],
                year=data["year"],
                condition=data["condition"],
                engine_type=data["engine_type"],
                engine_capacity=data["engine_capacity"],
                region=data["region"],
                city=data["city"],
                price_br=data["price_br"],
                price_usd=data["price_usd"],
                date_time_ad=data["date_time_ad"],
            )
            session.add(params)
            await session.commit()

    @staticmethod
    async def get_params_user(tg_id: int):
        async with session_maker() as session:
            query = select(User).where(User.tg_id == tg_id)
            result: User | None = await session.scalar(query)
            return result

    @staticmethod
    async def get_ads_av(tg_id: int):
        async with session_maker() as session:
            query = select(Av).where(Av.tg_id == tg_id)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_ads_kufar(tg_id: int):
        async with session_maker() as session:
            query = select(Kufar).where(Kufar.tg_id == tg_id)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def dell_ads_av(tg_id: int) -> None:
        async with session_maker() as session:
            query = delete(Av).where(Av.tg_id == tg_id)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def dell_ads_kufar(tg_id: int) -> None:
        async with session_maker() as session:
            query = delete(Kufar).where(Kufar.tg_id == tg_id)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def update_period_user(tg_id: int) -> None:
        async with session_maker() as session:
            # format column tracking_date in table str
            update_tracking_date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            query = update(User).where(User.tg_id == tg_id).values(tracking_date=update_tracking_date)
            await session.execute(query)
            await session.commit()
