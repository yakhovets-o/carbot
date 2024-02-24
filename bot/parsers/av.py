import datetime
import time

import requests
from requests.exceptions import RequestException


from bot.parsers.base_pars import BaseParser


class Av(BaseParser):

    def __init__(self) -> None:
        super().__init__()

        self.page_count = {}
        self.urls = {}

        self._get_url()

    def _get_url(self) -> dict | RequestException:

        if self.currency == 'Br':
            params = {'price_byn[min]': self.price_min, 'price_byn[max]': self.price_max, 'sort': 4}
        else:
            params = {'price_usd[min]': self.price_min, 'price_usd[max]': self.price_max, 'sort': 4}

        type_cars = {'cars' if self.cars else 'truck', 'truck' if self.truck_cars else 'cars'}

        try:
            for type_car in type_cars:
                url = f'https://api.av.by/offer-types/{type_car}/filters/main/init?'
                request = requests.get(url=url, params=params, headers=self.HEADERS)

                count_page = int(request.json()['pageCount'])
                response = request.url

                self.page_count.setdefault(type_car, count_page)
                self.urls.setdefault(type_car, response)

                time.sleep(2)

        except requests.exceptions.RequestException as errex:
            return errex

    @staticmethod
    def _get_date_ad(date: str) -> datetime:
        time_post_obj = datetime.datetime.strptime(date.replace('T', ' ').split('+')[0], '%Y-%m-%d %H:%M:%S') + \
                        datetime.timedelta(hours=3)

        return time_post_obj

    def _get_ads_cars(self, pages: int, url_cars: str) -> tuple | RequestException:

        try:
            for page in range(1, pages + 1):
                page_url = requests.get(url=url_cars, params={'page': page}, headers=self.HEADERS)

                time.sleep(2)

                cars = page_url.json()

                for car in cars['adverts']:
                    publ_ads = self._get_date_ad(car['refreshedAt'])
                    if publ_ads > self.tracking_date:
                        brand = car['metadata']['brandSlug']
                        model = car['metadata']['modelSlug']
                        year = car['metadata']['year']
                        condition = car['metadata']['condition']['label']

                        region = car['locationName']
                        city = car['shortLocationName']

                        price_br = car['price']['byn']['amount']
                        price_usd = car['price']['usd']['amount']

                        link = car['publicUrl']
                        print(brand, model, year, condition, region, city, price_usd, price_br, link, publ_ads,
                              sep='\n')
                        print('-------------------------------------------------------------------------------')
                    else:
                        break
                break
        except requests.exceptions.RequestException as errex:
            return errex

    def get_cars(self):
        url_cars = self.urls.get('cars', False)
        pages = self.page_count.get('cars', 0)

        if not url_cars:
            return f'По вашим параметрам объявлений не обнаружено'
        return self._get_ads_cars(pages=pages, url_cars=url_cars)

    def get_truck_cars(self):
        url_cars = self.urls.get('truck_cars', False)
        pages = self.page_count.get('truck_cars', 0)

        if not url_cars:
            return f'По вашим параметрам объявлений не обнаружено'
        return self._get_ads_cars(pages=pages, url_cars=url_cars)


av = Av()
print(av.get_cars())
print(av.get_truck_cars())
