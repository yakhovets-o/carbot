import datetime
from abc import ABC, abstractmethod


class BaseParser(ABC):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',

        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',

    }

    def __init__(self,
                 tg_id: int = 6165,
                 cars: bool = 1,
                 truck_cars: bool = 1,
                 currency: str = 'Usd',
                 price_min: int = 0,
                 price_max: int = 300,
                 update_period_min: int = 20,
                 tracking_date: str = '2024-02-21 16:05:00') -> None:
        self.tg_id = tg_id
        self.cars = cars
        self.truck_cars = truck_cars
        self.currency = currency
        self.price_min = price_min
        self.price_max = price_max
        self.update_period_min = update_period_min
        self.tracking_date = datetime.datetime.strptime(tracking_date, '%Y-%m-%d %H:%M:%S')

    @abstractmethod
    def _get_url(self) -> NotImplemented:
        raise NotImplementedError('the _get_url method is not defined in the class')

    @staticmethod
    @abstractmethod
    def _get_date_ad(date: str) -> NotImplemented:
        raise NotImplementedError('the _get_date_ad method is not defined in the class')

    @abstractmethod
    def get_cars(self) -> NotImplemented:
        raise NotImplementedError('the get_cars method is not defined in the class')

    @abstractmethod
    def get_truck_cars(self) -> NotImplemented:
        raise NotImplementedError('the get_truck_cars method is not defined in the class')
