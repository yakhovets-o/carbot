import aiogram.utils.markdown as fmt

from datetime import datetime

from aiogram import types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.keyboards.type_cars import type_car_kb
from bot.keyboards.currency_cars import cur_car_kb
from bot.db.orm_query import OrmQuery

from sqlalchemy.ext.asyncio import AsyncSession


class ParamSearch(StatesGroup):
    car = State()
    currency = State()
    min_price = State()
    max_price = State()
    tracking_date = State()


async def param_search(message: types.Message, state: FSMContext):
    await message.answer(text=fmt.hitalic('Выберите авто:'), reply_markup=type_car_kb)
    await state.set_state(ParamSearch.car)


async def car_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if not current_state:
        return

    await state.clear()
    await message.answer(text=fmt.hitalic('Действие отменено.'))


async def car_message(message: types.Message):
    text = fmt.text(
        fmt.text(fmt.hitalic('Укажите что то из предложенных вариантов')),
        fmt.text(fmt.hbold('/break '), fmt.hitalic('Для отмены поиска')),
        sep='\n\n'
    )
    await message.answer(text=text)
    await message.delete()


async def car_choice(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'Лекговое авто':
        await state.update_data(cars=True)
    if call.data == 'Грузовое авто':
        await state.update_data(truck_cars=True)

    if call.data == 'Лекговое авто / Грузовое авто':
        await state.update_data(cars=True)
        await state.update_data(truck_cars=True)

    data = await state.get_data()
    car = 'Легкое авто' if data.get("cars", False) else 'Грузовое авто'
    truck_car = 'Грузовое авто' if data.get("truck_cars", False) else 'Легкое авто'
    join_cars = ', '.join({car, truck_car})
    await state.update_data(join_cars=join_cars)
    data = await state.get_data()

    text = fmt.text(
        fmt.text(fmt.hitalic('Авто: ', data.get('join_cars'))),
        fmt.text(fmt.hbold('/break '), fmt.hitalic('Для отмены поиска')),
        sep='\n\n'
    )
    await call.message.answer(text=text)
    await call.message.edit_reply_markup()
    await state.set_state(ParamSearch.currency)
    await call.message.answer(text=fmt.hitalic('Выберите валюту.'), reply_markup=cur_car_kb)
    await call.answer()


async def currency_car(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'Usd':
        await state.update_data(currency='Usd')
    else:
        await state.update_data(currency='Br')

    data = await state.get_data()
    currency = data.get('currency')
    text = fmt.text(
        fmt.text(fmt.hitalic('Валюта: ', currency)),
        fmt.text(fmt.hbold('/break '), fmt.hitalic('Для отмены поиска')),
        sep='\n\n'
    )
    await call.message.answer(text=text)
    await call.message.edit_reply_markup()
    await state.set_state(ParamSearch.min_price)
    await call.message.answer(text=fmt.hitalic('💵 Введите минимальную стоимость.'))
    await call.answer()


async def car_price_start(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(price_min=int(message.text))

        await state.set_state(ParamSearch.max_price)

        await message.answer(text=fmt.hitalic('💸 Введите максимальную стоимость.'))

    else:
        await message.answer(text=fmt.hitalic('Введите целое число.'))
        await message.delete()


async def car_price_finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    price_min = data.get('price_min')

    if not message.text.isdigit():
        await message.answer(text=fmt.hitalic('Введите целое число.'))
        await message.delete()
    if message.text.isdigit() and price_min > int(message.text):
        await message.answer(text=fmt.hitalic('Максимальная стоимость должна привышать минимальную.'))
        await message.delete()
    if message.text.isdigit() and price_min <= int(message.text):
        await state.update_data(price_max=int(message.text))

        await state.set_state(ParamSearch.tracking_date)

        text = fmt.text(
            fmt.text(fmt.hitalic(f'Введите дату в формате  ДД.ММ.ГГ ЧЧ:MM '
                                 f'(например, {datetime.now().strftime("%d.%m.%y %H:%M")})')),
            fmt.text(fmt.hbold('/break '), fmt.hitalic('Для отмены поиска')),
            sep='\n\n'
        )

        await message.answer(text=text)


async def car_tracking_date(message: types.Message, state: FSMContext, session: AsyncSession):
    tracking_date_str = message.text

    try:
        date = str(datetime.strptime(tracking_date_str, '%d.%m.%y %H:%M'))
    except ValueError:
        await message.answer(text=fmt.hitalic('Дата некорректна'))
    else:
        await state.update_data(tracking_date=date)
        await state.update_data(user_id=message.from_user.id)

        data = await state.get_data()

        cars = data.get('join_cars')
        currency = data.get('currency')
        price_min = data.get('price_min')
        price_max = data.get('price_max')
        tracking_date = data.get("tracking_date")

        search = fmt.text(
            fmt.text(fmt.hbold('Критерии поиска: ')),
            fmt.text(fmt.hbold('Вы выбрали: ')),
            fmt.text(fmt.hbold('Авто 🚗 '), fmt.hitalic(cars)),
            fmt.text(fmt.hbold('Минимальная стоимость 💵 '), fmt.hitalic(price_min, currency)),
            fmt.text(fmt.hbold('Максимальная стоимость 💵 '), fmt.hitalic(price_max, currency)),
            fmt.text(fmt.hbold('Период публикации с 📅 '), fmt.hitalic(tracking_date)),
            sep='\n'
        )
        commands = fmt.text(
            fmt.text(fmt.hbold('Для получения результата '), fmt.hitalic('/get')),
            fmt.text(fmt.hbold('Для изменения параметров '), fmt.hitalic('/begin')),
            fmt.text(fmt.hbold('Для отмены поиска '), fmt.hitalic('/break')),
            sep='\n\n'

        )
        await message.answer(text=search)
        await message.answer(text=commands)

        # User table
        await OrmQuery.add_or_update_params(session=session, data=data)
        await state.clear()
