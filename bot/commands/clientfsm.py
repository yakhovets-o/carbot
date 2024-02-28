from datetime import datetime

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import types

from bot.keyboards.type_cars import type_car_kb
from bot.keyboards.currency_cars import cur_car_kb
from bot.db.orm_query import add_params

from sqlalchemy.ext.asyncio import AsyncSession


class ParamSearch(StatesGroup):
    car = State()
    currency = State()
    min_price = State()
    max_price = State()
    tracking_date = State()
    update_period_min = State()


async def param_search(message: types.Message, state: FSMContext):
    await message.answer(text='<b><i>выберите авто:</i></b>', reply_markup=type_car_kb)
    await state.set_state(ParamSearch.car)


async def car_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if not current_state:
        return

    await state.clear()
    await message.answer(text='<i>Действие отменено.</i>')


async def car_message(message: types.Message):
    await message.answer(text=f'🔨 <b><i>Укажите что то из предложенных вариантов\n\n'
                              f'Для отмены поиска вызовите команду</i></b> /break')
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
    cars = 'Выбрано' if data.get("cars", False) else 'Не выбрано'
    truck_cars = 'Выбрано' if data.get("truck_cars", False) else 'Не выбрано'

    await call.message.answer(text=f'<i>Легковое авто - {cars}\nГрузовое авто - {truck_cars}.</i>\n\n'
                                   f'<b>Для отмены поиска вызовите команду</b> /break')
    await call.message.edit_reply_markup()
    await state.set_state(ParamSearch.currency)
    await call.message.answer(text=f'💵 <i>Выберите валюту.</i>', reply_markup=cur_car_kb)
    await call.answer()


async def currency_car(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'Usd':
        await state.update_data(currency='Usd')
    else:
        await state.update_data(currency='Br')

    data = await state.get_data()
    currency = data.get('currency')
    await call.message.answer(text=f'<i>Валюта: {currency}</i>\n\n'
                                   f'<b>Для отмены поиска вызовите команду</b> /break')
    await call.message.edit_reply_markup()
    await state.set_state(ParamSearch.min_price)
    await call.message.answer(text=f'💵 <i>Введите минимальную стоимость.</i>')
    await call.answer()


async def car_price_start(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(price_min=int(message.text))

        await state.set_state(ParamSearch.max_price)

        await message.answer(text=f'💸 <i>Введите максимальную стоимость.</i>\n\n'
                                  f'<b>Для отмены поиска вызовите команду</b> /break')

    else:
        await message.answer(text=f'<b>Введите целое число</b>')
        await message.delete()


async def car_price_finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    price_min = data.get('price_min')

    if not message.text.isdigit():
        await message.answer(text=f'<b>Введите целое число.</b>')
        await message.delete()
    if message.text.isdigit() and price_min > int(message.text):
        await message.answer(text=f'<b>Максимальная стоимость должна привышать минимальную.</b>')
        await message.delete()
    if message.text.isdigit() and price_min <= int(message.text):
        await state.update_data(price_max=int(message.text))

        await state.set_state(ParamSearch.tracking_date)

        await message.answer(
            text=f'📅<b><i>Введте дату в формате  ДД.ММ.ГГ ЧЧ:MM (например, {datetime.now().strftime("%d.%m.%y %H:%M")})</i></b>\n\n'
                 f'<b>Для отмены поиска вызовите команду</b> /break')


async def car_tracking_date(message: types.Message, state: FSMContext):
    tracking_date_str = message.text

    try:
        date = str(datetime.strptime(tracking_date_str, '%d.%m.%y %H:%M'))
    except Exception:
        await message.answer(
            text=f'📅<b><i>Введте дату в формате  ДД.ММ.ГГ ЧЧ:MM (например, {datetime.now().strftime("%d.%m.%y %H:%M")})</i></b>\n\n'
                 f'<b>Для отмены поиска вызовите команду</b> /break')
    else:
        await state.update_data(tracking_date=date)
        await state.set_state(ParamSearch.update_period_min)

        await message.answer(text=f'⏰ <b><i>Укажите период  обновления  в минутах</i></b>\n\n'
                                  f'<b>Для отмены поиска вызовите команду</b> /break')


async def update_period_min(message: types.Message, state: FSMContext, session: AsyncSession):
    if not message.text.isdigit():
        await message.answer(f'<b>Введите целое число</b>')
        await message.delete()

    else:
        await state.update_data(update_period_min=int(message.text))
        await state.update_data(user_id=message.from_user.id)

        data = await state.get_data()
        print(data)

        cars = 'Выбрано' if data.get("cars", False) else 'Не выбрано'
        truck_cars = 'Выбрано' if data.get("truck_cars", False) else 'Не выбрано'
        currency = data.get('currency')
        await message.answer(f'<b>Критерии поиска:</b>\n'
                             f'<i>Вы выбрали:</i>\n'
                             f'<i>Лекговое авто - 🚗 <b>{cars}</b>\n</i>'
                             f'<i>Грузовое авто - 🚚 <b>{truck_cars}</b>\n</i>'
                             f'<i>Минимальная стоимость 💵 {data.get("price_min")} <b>{currency}</b></i>\n'
                             f'<i>Максимальная стоимость 💸 {data.get("price_max")} <b>{currency}</b></i>\n'
                             f'<i>Период публикации с 📅{data.get("tracking_date")}</i>\n'
                             f'<i>Период обновления ⏰ {data.get("update_period_min")} <b>min</b></i>\n\n'
                             f'<b>Для получения результата вызовите команду</b> /get \n\n'
                             f'<b>Для изменения параметров поиска вызовите команду</b> /begin\n'
                             f'<b>Для отмены поиска вызовите команду</b> /break'
                             )

        await add_params(session=session, data=data)
        await state.clear()
