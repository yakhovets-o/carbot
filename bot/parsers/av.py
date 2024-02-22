import datetime
import time

import requests


class Av:
    cookies = {
        '_ga_GWM6BXJZNK': 'GS1.1.1708549349.9.0.1708549349.0.0.0',
        '_ga': 'GA1.1.115487787.1689690249',
        '__gads': 'ID=2f7ef2b02daf11f3:T=1689690242:RT=1708521649:S=ALNI_MYjr0kOFw_JeBHcLtBsMWvtNdvQvQ',
        '__gpi': 'UID=00000c3ed84f8078:T=1689690242:RT=1708521649:S=ALNI_MaAWqGaqL35NpyrVXxN9vpOzdxV4w',
        '_ym_uid': '1707589397848967946',
        '_ym_d': '1707589397',
        'acceptedCookies': '{^%^22analytical^%^22:false^%^2C^%^22promotion^%^22:false^%^2C^%^22technical^%^22:'
                           'true^%^2C^%^22accepted^%^22:true}',
        '_fbp': 'fb.1.1707589399083.656541358',
        '__eoi': 'ID=6d8498fbd332cbda:T=1707589313:RT=1708521649:S=AA-AfjZgVrV0wVUsPYDuBqju6uXK',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        # 'Cookie': '_ga_GWM6BXJZNK=GS1.1.1708549349.9.0.1708549349.0.0.0; _ga=GA1.1.115487787.1689690249;
        # __gads=ID=2f7ef2b02daf11f3:T=1689690242:RT=1708521649:S=ALNI_MYjr0kOFw_JeBHcLtBsMWvtNdvQvQ;
        # __gpi=UID=00000c3ed84f8078:T=1689690242:RT=1708521649:S=ALNI_MaAWqGaqL35NpyrVXxN9vpOzdxV4w;
        # _ym_uid=1707589397848967946; _ym_d=1707589397;
        # acceptedCookies={^%^22analytical^%^22:false^%^2C^%^22promotion^%^22:false^%^2C^%^22technical^%^22:
        # true^%^2C^%^22accepted^%^22:true};
        # _fbp=fb.1.1707589399083.656541358; __eoi=ID=6d8498fbd332cbda:T=1707589313:RT=1708521649:
        # S=AA-AfjZgVrV0wVUsPYDuBqju6uXK',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
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

        self.page_count = {}
        self.urls = {}

    def get_url(self):

        if self.currency == 'Br':
            params = {'price_byn[min]': self.price_min, 'price_byn[max]': self.price_max, 'sort': 4}
        else:
            params = {'price_usd[min]': self.price_min, 'price_usd[max]': self.price_max, 'sort': 4}

        type_cars = {'cars' if self.cars else 'truck', 'truck' if self.truck_cars else 'cars'}

        try:
            for type_car in type_cars:
                url = f'https://api.av.by/offer-types/{type_car}/filters/main/init?'
                request = requests.get(url=url, params=params, headers=self.headers, cookies=self.cookies)

                count_page = int(request.json()['pageCount'])
                url = request.url

                self.page_count.setdefault(type_car, count_page)
                self.urls.setdefault(type_car, url)

                time.sleep(5)
            # return self.urls, self.page_count
        except requests.exceptions.RequestException as errex:
            return errex

    @staticmethod
    def get_time_post(time_post: str) -> datetime:
        time_post_obj = datetime.datetime.strptime(time_post.replace('T', ' ').split('+')[0], '%Y-%m-%d %H:%M:%S') + \
                        datetime.timedelta(hours=3)

        return time_post_obj

    def ads_cars(self):

        url_cars = self.urls.get('cars', False)
        pages = self.page_count.get('cars', 0)

        if not url_cars:
            return f'По вашим параметрам объявлений не обнаружено'

        for page in range(1, pages + 1):
            page_url = requests.get(url=url_cars, params={'page': page}, headers=self.headers, cookies=self.cookies)

            time.sleep(5)

            cars = page_url.json()

            for car in cars['adverts']:
                publ_ads = self.get_time_post(car['refreshedAt'])
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
                    print(brand, model, year, condition, region, city, price_usd, price_br, link, publ_ads, sep='\n')
                    print('-------------------------------------------------------------------------------')
                else:
                    break
            break


av = Av()
print(av.get_url())
print(av.ads_cars())
