from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

type_car_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🚗 Легковое авто', callback_data='Легковое авто'),
            InlineKeyboardButton(text='🚚 Грузовое авто', callback_data='Грузовое авто'),

        ],
        [
            InlineKeyboardButton(text='🚗 Легковое авто / 🚚 Грузовое авто',
                                 callback_data='Легковое авто / Грузовое авто')
        ]
    ],

)
