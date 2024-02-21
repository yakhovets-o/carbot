from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

type_car_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🚗 Лекговое авто', callback_data='Лекговое авто'),
            InlineKeyboardButton(text='🚚 Грузовое авто', callback_data='Грузовое авто'),

        ],
        [
            InlineKeyboardButton(text='🚗 Лекговое авто / 🚚 Грузовое авто',
                                 callback_data='Лекговое авто / Грузовое авто')
        ]
    ],

)
