import aiogram.utils.markdown as fmt
from aiogram import types


async def mess_other(message: types.Message):
    text = fmt.text(
        fmt.text(fmt.hitalic("Команда некорректна: ")),
        fmt.text(fmt.hitalic("Список команд: "), fmt.hbold("/help")),
        sep="\n\n",
    )
    await message.answer(text=text)

    await message.delete()
