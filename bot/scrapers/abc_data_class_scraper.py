import datetime

from fake_useragent import UserAgent

from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass()
class AbcDataClassScraper(ABC):
    tg_id: int
    cars: bool
    truck_cars: bool
    currency: str
    price_min: int
    price_max: int
    tracking_date: str

    type_cars: set = field(init=False, repr=False)
    type_currency: str = field(init=False)
    params: dict = field(init=False, repr=False)

    __user_agent = UserAgent().random

    def __post_init__(self):
        if self.__class__.__name__ == 'Av':
            self.type_cars = {'cars' if self.cars else 'truck', 'truck' if self.truck_cars else 'cars'}
            self.currency = 'byn' if self.currency == 'Br' else 'usd'

            # query parameter url
            self.params = {f'price_{self.currency}[min]': self.price_min,
                           f'price_{self.currency}[max]': self.price_max, 'sort': 4}

        if self.__class__.__name__ == 'Kufar':

            # 2010 category cars, 2060 category truck cars
            self.type_cars = {2010 if self.cars else 2060, 2060 if self.truck_cars else 2010}

            # query parameter url
            self.params = {'cur': self.currency, 'size': 30, 'sort': 'lst.d', 'typ': 'sell',
                           'lang': 'ru'}

            self.currency = 'USD' if self.currency == 'Usd' else 'BYR'

            if self.currency == 'BYR':
                # the digit of the number by 2  for example 300 == 3, 30_000 == 300
                self.price_min = self.price_min * 100
                self.price_max = self.price_max * 100

    HEADERS = {
        'User-Agent': __user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',

        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',

    }

    @staticmethod
    @abstractmethod
    def _get_date_ad(date: str) -> NotImplemented:
        raise NotImplementedError('the _get_date_ad method is not defined in the class')

    @staticmethod
    @abstractmethod
    def _get_properties_ad(properties: str) -> NotImplemented:
        raise NotImplementedError('the _get_properties_ad method is not defined in the class')

    @abstractmethod
    def _get_ads(self, session, page_url: str) -> NotImplemented:
        raise NotImplementedError('the _get_ads method is not defined in the class')

    @abstractmethod
    def create_task(self) -> NotImplemented:
        raise NotImplementedError('the _create_task method is not defined in the class')



