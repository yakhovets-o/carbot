from aiogram import types


async def mess_other(message: types.Message):
    await message.answer(f'Команда некорректна\n'
                         f'Список команд можно получить по команде /help')

    await message.delete()
