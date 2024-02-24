import time
import datetime

import requests
from requests.exceptions import RequestException

from bot.parsers.base_pars import BaseParser


class Kufar(BaseParser):
    TYPE = 'sell'
    SORT = 'lst.d'
    LANG = 'ru'
    SIZE = 30

    def __init__(self) -> None:
        super().__init__()

        self.urls = self._get_url()

    def _get_url(self) -> dict | RequestException:
        self.currency = 'USD' if self.currency == 'Usd' else 'BYR'

        if self.currency == 'BYR':
            self.price_min = self.price_min * 100
            self.price_max = self.price_max * 100

        # 2010 category cars, 2060 category truck cars
        type_cars = {2010 if self.cars else 2060, 2060 if self.truck_cars else 2010}

        params = {'cur': self.currency, 'size': self.SIZE, 'sort': self.SORT, 'typ': self.TYPE,
                  'lang': self.LANG}

        url = f'https://api.kufar.by/search-api/v1/search/rendered-paginated?' \
              f'prc=r%3A{self.price_min}%2C{self.price_max}'

        cars_url = {}

        for type_car in type_cars:
            params.update(cat=type_car)

            request = requests.get(url=url, params=params, headers=self.HEADERS)
            response = request.url
            time.sleep(3)

            pages = request.json()['pagination']['pages']

            urls = []

            for page in pages:
                if not page['token']:
                    urls.append(response)
                else:

                    # create query parameter
                    token = '&cursor=' + str(page['token'][:-2]) + '%3D%3D'

                    url_page = requests.get(url=response + token, headers=self.HEADERS)
                    urls.append(url_page.url)

            cars_url.setdefault(type_car, urls)

        return cars_url

    @staticmethod
    def _get_date_ad(date: str) -> datetime:
        date_obj = datetime.datetime.strptime(date.replace('T', ' ')[:-1], '%Y-%m-%d %H:%M:%S') + \
                   datetime.timedelta(hours=3)

        return date_obj

    @staticmethod
    def _get_price_usd(price_usd: str) -> int:
        price_usd = int(price_usd[:-2] if len(price_usd) > 2 else 0)

        return price_usd

    @staticmethod
    def _get_price_br(price_br: str) -> int:
        price_br = int(price_br[:-2] if len(price_br) > 2 else 0)

        return price_br

    @staticmethod
    def _get_parameters(parameters: dict) -> dict:

        all_parameters = {'Марка': 'Не указано', 'Модель': 'Не указано', 'Год': 'Не указано',
                          'Тип двигателя': 'Не указано', 'Объем, л': 'Не указано', 'Область': 'Не указано',
                          'Город / Район': 'Не указано'}

        for param in parameters:
            if param['pl'] in all_parameters:
                all_parameters[param['pl']] = param['vl']

        return all_parameters

    def _get_ads_cars(self, url_cars: list) -> tuple | RequestException:

        try:
            for url in url_cars:

                request = requests.get(url=url, headers=self.HEADERS)

                page = request.json()
                time.sleep(3)

                for ad in page['ads']:
                    date = self._get_date_ad(ad['list_time'])
                    if date > self.tracking_date:

                        brand = self._get_parameters(ad['ad_parameters']).get('Марка')
                        model = self._get_parameters(ad['ad_parameters']).get('Модель')

                        year = self._get_parameters(ad['ad_parameters']).get('Год')
                        type_engine = self._get_parameters(ad['ad_parameters']).get('Тип двигателя')
                        volume = self._get_parameters(ad['ad_parameters']).get('Объем, л')

                        price_br = self._get_price_br(ad['price_byn'])
                        price_usd = self._get_price_usd(ad['price_usd'])

                        region = self._get_parameters(ad['ad_parameters']).get('Область')
                        city = self._get_parameters(ad['ad_parameters']).get('Город / Район')

                        link = ad['ad_link']

                        print(brand, model, year, type_engine, volume, price_br, price_usd, region,
                              city, link, date, sep='\n')
                        print('--------------------------------------------------------------')

                    else:
                        break
                break

        except requests.exceptions.RequestException as errex:
            return errex

    def get_cars(self):
        cars_urls = self.urls.get(2010, False)
        if cars_urls:
            return self._get_ads_cars(url_cars=cars_urls)

    def get_truck_cars(self):
        truck_cars_urls = self.urls.get(2060, False)
        if truck_cars_urls:
            return self._get_ads_cars(url_cars=truck_cars_urls)


kufar = Kufar()
print(kufar.get_cars())

print(kufar.get_truck_cars())
