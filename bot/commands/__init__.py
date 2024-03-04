__all__ = ['register_client_command', 'register_client_command_fsm', 'register_client_command_other']

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter

from bot.commands.client import start, contacts, supports, helper, sub, get, params

from bot.commands.clientfsm import (ParamSearch, param_search, car_cancel,
                                    car_message, car_choice, car_price_start,
                                    car_price_finish, currency_car, car_tracking_date)

from bot.commands.other import mess_other


def register_client_command(router: Router) -> None:
    router.message.register(start, CommandStart())
    router.message.register(params, Command('params'))
    router.message.register(contacts, Command('contacts'))
    router.message.register(supports, Command('supports'))
    router.message.register(sub, Command('sub'))
    router.message.register(helper, Command('help'))
    router.message.register(get, Command('get'))


def register_client_command_fsm(router: Router) -> None:
    router.message.register(param_search, StateFilter(None), Command('begin'))

    router.message.register(car_cancel, StateFilter('*'), Command('break'))
    router.message.register(car_cancel, StateFilter('*'), F.text.casefold() == 'break')

    router.message.register(car_message, StateFilter(ParamSearch.car))
    router.callback_query.register(car_choice, StateFilter(ParamSearch.car))

    router.message.register(car_message, StateFilter(ParamSearch.currency))
    router.callback_query.register(currency_car, StateFilter(ParamSearch.currency))

    router.message.register(car_price_start, StateFilter(ParamSearch.min_price))

    router.message.register(car_price_finish, StateFilter(ParamSearch.max_price))

    router.message.register(car_tracking_date, StateFilter(ParamSearch.tracking_date))


def register_client_command_other(router: Router) -> None:
    router.message.register(mess_other)
