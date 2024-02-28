import os

from aiogram import types

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.orm_query import get_params_user

from bot.scrapers.av import Av


async def start(message: types.Message) -> None:
    your_name = message.from_user.full_name
    time_message_hour = (message.date.time().hour + 3) % 24
    time_of_day = {'Доброе утро': tuple(range(4, 12)), 'Добрый день': tuple(range(12, 17)),
                   'Добрый вечер': tuple(range(17, 24)), 'Доброй ночи': tuple(range(0, 4))}

    text = f'{tuple(k for k, v in time_of_day.items() if time_message_hour in v)[0]} <b><i>{your_name}</i></b> ! \n' \
           f'Для указания  параметров поиска вызовите команду /begin'
    await message.answer(text=text)


async def contacts(message: types.Message) -> None:
    await message.answer(text=f'<b>Admin:</b> {os.getenv("admin")}')


async def supports(message: types.Message) -> None:
    await message.answer(text=f'<b>Поддержка бота:</b>  {os.getenv("support")}')


async def sub(message: types.Message) -> None:
    await message.answer(text=f'На данный момент подписка недоступна')


async def helper(message: types.Message) -> None:
    await message.answer(text=f'<b>Полный список команд:</b>\n'
                              f'/start - <i>Запуск бота</i>\n'
                              f'/contacts - <i>Контакты для связи</i>\n'
                              f'/supports - <i>Написать в поддержку</i>\n'
                              f'/sub - <i>оплата подписки</i>\n'
                              f'/begin - <i>Параметры поиска</i>'
                         )


async def get(message: types.Message, session: AsyncSession):
    await message.answer('Пожалуйста подождите...')
    tg_id = message.from_user.id

    params_value = await get_params_user(session=session, tg_id=tg_id)
    params_key = ('tg_id', 'cars', 'truck_cars', 'currency',
                  'price_min', 'price_max', 'update_period_min', 'tracking_date')

    params_dict = dict(zip(params_key, params_value[0]))

    tg_id = params_dict['tg_id']
    cars = params_dict['cars']
    truck_cars = params_dict['truck_cars']
    currency = params_dict['currency']
    price_min = params_dict['price_min']
    price_max = params_dict['price_max']
    update_period_min = params_dict['update_period_min']
    tracking_date = params_dict['tracking_date']

    av  = Av()
    print(av)


async def mess_other(message: types.Message) -> None:
    await message.answer(f'Команда некорректна\n'
                         f'Список команд можно получить по команде /help')
    await message.delete()
