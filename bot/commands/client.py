import os
import aiogram.utils.markdown as fmt

from aiogram import types

from arq import ArqRedis

from datetime import timedelta


async def start(message: types.Message) -> None:
    your_name = message.from_user.full_name
    time_message_hour = (message.date.time().hour + 3) % 24
    time_of_day = {'Доброе утро': tuple(range(4, 12)), 'Добрый день': tuple(range(12, 17)),
                   'Добрый вечер': tuple(range(17, 24)), 'Доброй ночи': tuple(range(0, 4))}
    text = fmt.text(
        fmt.text(fmt.hbold(tuple(k for k, v in time_of_day.items() if time_message_hour in v)[0], your_name)),
        fmt.text(fmt.hitalic('Для указания параметров поиска'), fmt.hbold('/begin')),
        sep='\n\n'

    )

    await message.answer(text=text)


async def contacts(message: types.Message) -> None:
    await message.answer(text=fmt.text(fmt.hitalic('Admin: '), fmt.hbold(os.getenv('admin'))))


async def supports(message: types.Message) -> None:
    await message.answer(text=fmt.text(fmt.hitalic('Поддержка бота: '), fmt.hbold(os.getenv('support'))))


async def sub(message: types.Message) -> None:
    await message.answer(text=fmt.hitalic('На данный момент подписка недоступна'))


async def helper(message: types.Message) -> None:
    commands = fmt.text(
        fmt.text(fmt.hbold('Полный список команд: ')),
        fmt.text(fmt.hbold('/start'), fmt.hitalic(' - Запуск бота')),
        fmt.text(fmt.hbold('/contacts'), fmt.hitalic(' - Контакты для связи')),
        fmt.text(fmt.hbold('/supports'), fmt.hitalic(' - Написать в поддержку')),
        fmt.text(fmt.hbold('/sub'), fmt.hitalic(' - оплата подписки')),
        fmt.text(fmt.hbold('/begin'), fmt.hitalic(' - Параметры поиска')),
        fmt.text(fmt.hbold('/get'), fmt.hitalic(' - результат поиска')),
        sep='\n'

    )
    await message.answer(text=commands)


async def get(message: types.Message, arqredis: ArqRedis) -> None:
    await message.answer(text=fmt.hitalic('Пожалуйста подождите...'))
    tg_id = message.from_user.id

    # background task path  bot/scheduler
    await arqredis.enqueue_job('get', _defer_by=timedelta(seconds=5), tg_id=tg_id)
