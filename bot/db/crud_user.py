from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.user_model import User


async def add_params(session: AsyncSession, data: dict):
    params = User(
        truck_cars=data.get('truck_cars', False),
        cars=data.get('cars', False),
        id=data.get('user_id'),
        currency=data.get('currency'),
        price_min=data.get('price_min'),
        price_max=data.get('price_max'),
        update_period_min=data.get('update_period_min'),
        tracking_date=data.get('tracking_date')

    )
    session.add(params)
    await session.commit()
