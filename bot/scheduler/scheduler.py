from aiogram import Bot
import os

from arq.connections import RedisSettings

from bot.db.orm_query import OrmQuery
from bot.db.models import User

from aiogram.utils.markdown import hbold, hlink
import asyncio

from bot.scrapers.av import Av
from bot.scrapers.kufar import Kufar

async def startup(ctx):
    ctx['bot'] = Bot(token='6210880019:AAHItwAko076rF_hnv2GP3bvk5lBRL4Mru4')


async def shutdown(ctx):
    await ctx['bot'].session.aclose()


async def get(ctx, tg_id: int):

    bot: Bot = ctx['bot']

    params_value: User = await OrmQuery.get_params_user(tg_id=tg_id)

    if params_value is None:
        await bot.send_message(tg_id, text='Для получения результатов, укажите критерии поиска')

    else:
        # # create av obj scraper
        # av = Av(params_value.tg_id,
        #         params_value.cars,
        #         params_value.truck_cars,
        #         params_value.currency,
        #         params_value.price_min,
        #         params_value.price_max,
        #         params_value.update_period_min,
        #         params_value.tracking_date
        #         )
        # # start av scraper
        # await av.create_task()
        # result av scraper
        ads_av = await OrmQuery.get_ads_av(tg_id=tg_id)
        #
        # # create kufar obj scraper
        # kufar = Kufar(params_value.tg_id,
        #               params_value.cars,
        #               params_value.truck_cars,
        #               params_value.currency,
        #               params_value.price_min,
        #               params_value.price_max,
        #               params_value.update_period_min,
        #               params_value.tracking_date
        #               )
        # # start kufar scraper
        # await kufar.create_task()

        # result kufar scraper
        ads_kufar = await OrmQuery.get_ads_kufar(tg_id=tg_id)

        # kufar + av result
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
                await bot.send_message(tg_id, text=card)
            await bot.send_message(tg_id, text='Поиск завершен.')

            # del av table
            await OrmQuery.dell_ads_av(tg_id=tg_id)
            # del kufar table
            await OrmQuery.dell_ads_kufar(tg_id=tg_id)
            # update search parameters
            await OrmQuery.update_period_user(tg_id=tg_id)

        else:
            await bot.send_message(tg_id, text='По вашему запросу объявлений не обнаружено.\n'
                                                       'Обновите параметры поиска командой \n/begin')


class WorkerSettings:
    redis_setting = RedisSettings()
    on_startup = startup
    on_shutdown = shutdown
    functions = [get]
