import asyncio
import aiogram.utils.markdown as fmt

from aiogram import Bot

from bot.config import BotConfig, RedisConfig
from bot.db.orm_query import OrmQuery
from bot.scrapers.av import Av
from bot.scrapers.kufar import Kufar


# init bot to send background task
async def startup(ctx):
    ctx['bot'] = Bot(token=BotConfig.token)


async def shutdown(ctx):
    await ctx['bot'].session.aclose()


# background task
async def get(ctx, tg_id: int):
    bot: Bot = ctx['bot']

    # get params for scraper User table
    params_value = await OrmQuery.get_params_user(tg_id=tg_id)

    if params_value is None:
        await bot.send_message(tg_id, text=fmt.hitalic('Для получения результатов, укажите критерии поиска'))

    else:
        # create av obj scraper
        av = Av(params_value.tg_id,
                params_value.cars,
                params_value.truck_cars,
                params_value.currency,
                params_value.price_min,
                params_value.price_max,
                params_value.tracking_date
                )

        # start av scraper
        await av.create_task()
        # result av scraper
        ads_av = await OrmQuery.get_ads_av(tg_id=tg_id)

        # create kufar obj scraper
        kufar = Kufar(params_value.tg_id,
                      params_value.cars,
                      params_value.truck_cars,
                      params_value.currency,
                      params_value.price_min,
                      params_value.price_max,
                      params_value.tracking_date
                      )

        # start kufar scraper
        await kufar.create_task()
        # result kufar scraper
        ads_kufar = await OrmQuery.get_ads_kufar(tg_id=tg_id)

        # kufar + av result
        ads_av_kufar = ads_av + ads_kufar

        if ads_av_kufar:
            for ad in ads_av_kufar:
                card = fmt.text(
                    fmt.text(fmt.hbold('Марка и модель: '), fmt.hlink((ad.brand + ' ' + ad.model), ad.link)),
                    fmt.text(fmt.hbold('Состояние: '), fmt.hitalic(ad.condition)),
                    fmt.text(fmt.hbold('Год: '), fmt.hitalic(ad.year)),
                    fmt.text(fmt.hbold('Тип двигателя и объем: '), fmt.hitalic(ad.engine_type, ad.engine_capacity)),
                    fmt.text(fmt.hbold('Дата и место публикации: '), fmt.hitalic(ad.date_time_ad, ad.region, ad.city)),
                    fmt.text(fmt.hbold('Цена: '), 'Br', fmt.hitalic(ad.price_br), 'Usd', fmt.hitalic(ad.price_usd)),
                    sep='\n'
                )
                await asyncio.sleep(1)
                await bot.send_message(tg_id, text=card, parse_mode='HTML')

            await bot.send_message(tg_id, text=fmt.hitalic('Поиск завершен.'), parse_mode='HTML')

            # del av table
            await OrmQuery.dell_ads_av(tg_id=tg_id)
            # del kufar table
            await OrmQuery.dell_ads_kufar(tg_id=tg_id)
            # update search parameters
            await OrmQuery.update_period_user(tg_id=tg_id)

        else:
            await bot.send_message(tg_id, text=fmt.text(
                fmt.text(fmt.hitalic('По вашему запросу объявлений не обнаружено.')),
                fmt.text(fmt.hitalic('Для обновления параметров поиска'), fmt.hbold(' /begin')),
                sep='\n\n'
            ), parse_mode='HTML'
                                   )


# it is executed in a separate thread
# path  arq bot.scheduler.scheduler.WorkerSettings
class WorkerSettings:
    redis_setting = RedisConfig.pool_settings
    on_startup = startup
    on_shutdown = shutdown
    functions = [get]
