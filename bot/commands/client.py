import os
from datetime import timedelta

import aiogram.utils.markdown as fmt
from aiogram import types
from arq import ArqRedis

from bot.db.orm_query import OrmQuery


async def start(message: types.Message) -> None:
    your_name = message.from_user.full_name
    time_message_hour = (message.date.time().hour + 3) % 24
    time_of_day = {
        "Доброе утро": tuple(range(4, 12)),
        "Добрый день": tuple(range(12, 17)),
        "Добрый вечер": tuple(range(17, 24)),
        "Доброй ночи": tuple(range(0, 4)),
    }
    text = fmt.text(
        fmt.text(
            fmt.hbold(
                tuple(k for k, v in time_of_day.items() if time_message_hour in v)[0],
                your_name,
            )
        ),
        fmt.text(fmt.hitalic("Для указания параметров поиска"), fmt.hbold("/begin")),
        sep="\n\n",
    )

    await message.answer(text=text)


async def get(message: types.Message, arqredis: ArqRedis) -> None:
    await message.answer(text=fmt.hitalic("Пожалуйста подождите..."))
    tg_id = message.from_user.id

    # background task path  bot/scheduler
    await arqredis.enqueue_job("get", _defer_by=timedelta(seconds=5), tg_id=tg_id)


async def params(message: types.Message) -> None:
    tg_id = message.from_user.id

    # get params for scraper User table
    params_value = await OrmQuery.get_params_user(tg_id=tg_id)
    if params_value is None:
        await message.answer(text=fmt.hitalic("Для получения результатов, укажите критерии поиска"))
        await message.answer(text=fmt.text(fmt.hitalic("Параметры поиска"), fmt.hbold(" /begin")))
    else:
        type_cars = f"{'Легковое' if params_value.cars else 'Грузовое' if params_value.truck_cars else 'Легковое'}"
        text = fmt.text(
            fmt.text(fmt.hbold("Тип: "), fmt.hitalic(type_cars, "авто")),
            fmt.text(
                fmt.hbold("Минимальная стоимость: "),
                fmt.hitalic(params_value.price_min),
            ),
            fmt.text(
                fmt.hbold("Максимальная стоимость: "),
                fmt.hitalic(params_value.price_max),
            ),
            fmt.text(
                fmt.hbold("Период публикации: "),
                fmt.hitalic(params_value.tracking_date),
            ),
            sep="\n",
        )

        await message.answer(text=text)
        await message.answer(text=fmt.text(fmt.hitalic("Параметры поиска"), fmt.hbold(" /begin")))


async def contacts(message: types.Message) -> None:
    await message.answer(text=fmt.text(fmt.hitalic("Admin: "), fmt.hbold(os.getenv("admin"))))


async def supports(message: types.Message) -> None:
    await message.answer(text=fmt.text(fmt.hitalic("Поддержка бота: "), fmt.hbold(os.getenv("support"))))


async def sub(message: types.Message) -> None:
    await message.answer(text=fmt.hitalic("На данный момент подписка недоступна"))


async def helper(message: types.Message) -> None:
    commands = fmt.text(
        fmt.text(fmt.hbold("Полный список команд: ")),
        fmt.text(fmt.hbold("/start"), fmt.hitalic(" - Запуск бота")),
        fmt.text(fmt.hbold("/contacts"), fmt.hitalic(" - Контакты для связи")),
        fmt.text(fmt.hbold("/supports"), fmt.hitalic(" - Написать в поддержку")),
        fmt.text(fmt.hbold("/sub"), fmt.hitalic(" - Оплата подписки")),
        fmt.text(fmt.hbold("/begin"), fmt.hitalic(" - Установить параметры поиска")),
        fmt.text(fmt.hbold("/get"), fmt.hitalic(" - Результат поиска")),
        fmt.text(fmt.hbold("/params"), fmt.hitalic(" - Получить параметры поиска")),
        sep="\n",
    )
    await message.answer(text=commands)
