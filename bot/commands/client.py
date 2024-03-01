import os
import asyncio

from aiogram import types
from aiogram.utils.markdown import hbold, hlink

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.orm_query import OrmQuery
from bot.db.models import User

from bot.scrapers.av import Av
from bot.scrapers.kufar import Kufar


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

    params_value: User = await OrmQuery.get_params_user(session=session, tg_id=tg_id)

    if params_value is None:
        await message.answer('Для получения результатов, укажите критерии поиска')
    else:
        # av = Av(params_value.tg_id,
        #         params_value.cars,
        #         params_value.truck_cars,
        #         params_value.currency,
        #         params_value.price_min,
        #         params_value.price_max,
        #         params_value.update_period_min,
        #         params_value.tracking_date
        #         )
        #
        # await av.create_task()

        ads_av = await OrmQuery.get_ads_av(session=session, tg_id=tg_id)

        # kufar = Kufar(params_value.tg_id,
        #               params_value.cars,
        #               params_value.truck_cars,
        #               params_value.currency,
        #               params_value.price_min,
        #               params_value.price_max,
        #               params_value.update_period_min,
        #               params_value.tracking_date
        #               )
        # await kufar.create_task()

        ads_kufar = await OrmQuery.get_ads_kufar(session=session, tg_id=tg_id)

        ads_av_kufar = ads_av + ads_kufar
        print(ads_av_kufar, '~~~~~~~~~~~~~~~~~~~~~~~~~~~~', type(ads_av_kufar))
        if ads_av_kufar:
            for ad in ads_av_kufar:
                card = f'{hbold("Марка и модель: ")} {hlink((ad.brand + " " + ad.model), ad.link)}\n' \
                       f'{hbold("Состояние: ")} {ad.condition}\n' \
                       f'{hbold("Год: ")} {ad.year}\n' \
                       f'{hbold("Тип двигателя и объем: ")} {ad.engine_type}, {ad.engine_capacity}\n' \
                       f'{hbold("Дата и место публикации: ")} {ad.date_time_ad}, {ad.region}, {ad.city}\n' \
                       f'{hbold("Цена: ")} Br {ad.price_br}, Usd {ad.price_usd}'

                await asyncio.sleep(1)
                await message.answer(card)
            await message.answer('Поиск завершен.')

            await OrmQuery.dell_ads_av(session=session, tg_id=tg_id)
            await OrmQuery.dell_ads_kufar(session=session, tg_id=tg_id)
            await OrmQuery.update_period_user(session=session, tg_id=tg_id)

        else:
            await message.answer('По вашему запросу объявлений не обнаружено.\n'
                                 'Обновите параметры поиска командой \n/begin')


async def mess_other(message: types.Message) -> None:
    await message.answer(f'Команда некорректна\n'
                         f'Список команд можно получить по команде \n/help')
    await message.delete()
