from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cur_car_kb = InlineKeyboardMarkup(

    inline_keyboard=[
        [InlineKeyboardButton(text='Usd', callback_data='Usd'),
         InlineKeyboardButton(text='Br', callback_data='Br')
         ]
    ]
)
