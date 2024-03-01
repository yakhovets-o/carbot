from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

begin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='get'),
            KeyboardButton(text='begin')
        ],
        [
            KeyboardButton(text='break')
        ]
    ],
    resize_keyboard=True, one_time_keyboard=True
)
