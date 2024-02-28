from sqlalchemy import select, delete

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User, Av, Kufar


async def add_params(session: AsyncSession, data: dict) -> None:
    params = User(
        truck_cars=data.get('truck_cars', False),
        cars=data.get('cars', False),
        tg_id=data.get('user_id'),
        currency=data.get('currency'),
        price_min=data.get('price_min'),
        price_max=data.get('price_max'),
        update_period_min=data.get('update_period_min'),
        tracking_date=data.get('tracking_date')

    )
    session.add(params)
    await session.commit()


async def add_kufar_ads(session: AsyncSession, data: dict) -> None:
    params = Kufar(
        link=data['link'],
        tg_id=data['tg_id'],
        brand=data['brand'],
        model=data['model'],
        year=data['year'],
        type_engine=data['type_engine'],
        volume=data['volume'],
        condition=data['condition'],
        region=data['region'],
        city=data['city'],
        price_br=data['price_br'],
        price_usd=data['price_usd'],
        date_time_post=data['date_time_post']
    )
    session.add(params)
    await session.commit()


async def add_av_ads(session: AsyncSession, data: dict) -> None:
    params = Av(
        link=data['link'],
        tg_id=data['tg_id'],
        brand=data['brand'],
        model=data['model'],
        year=data['year'],
        condition=data['condition'],
        region=data['region'],
        city=data['city'],
        price_br=data['price_br'],
        price_usd=data['price_usd'],
        date_time_post=data['date_time_post']
    )
    session.add(params)
    await session.commit()


async def get_params_user(session: AsyncSession, tg_id: int):
    query = select(User).where(User.tg_id == tg_id)
    result = await session.execute(query)
    return result.all()


async def get_ads_av_kufar(session: AsyncSession, tg_id: int) -> tuple:
    for model in [Av, Kufar]:
        query = select(model).where(model.tg_id == tg_id)
        result = await session.execute(query)
        yield result.all()


async def dell_ads_av_kufar(session: AsyncSession, tg_id: int) -> None:
    for model in [Av, Kufar]:
        query = delete(model).where(model.tg_id == tg_id)
        await session.execute(query)
        await session.commit()
