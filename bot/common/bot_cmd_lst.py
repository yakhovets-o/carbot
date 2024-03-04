from aiogram.types import BotCommand

bot_cmd_lst = [
    BotCommand(command='start', description='Запуск бота'),
    BotCommand(command='contacts', description='Контакты для связи'),
    BotCommand(command='supports', description='Написать в поддержку'),
    BotCommand(command='sub', description='Оплата подписки'),
    BotCommand(command='begin', description='Установить параметры поиска'),
    BotCommand(command='get', description='Результаты поиска'),
    BotCommand(command='params', description='Получить параметры поиска'),
    BotCommand(command='help', description='Список команд')

]
