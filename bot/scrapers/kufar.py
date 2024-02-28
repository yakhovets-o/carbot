import time
import datetime

import aiohttp
import asyncio

from typing import NoReturn

from bot.scrapers.abc_data_class_scraper import AbcDataClassScraper

start = time.perf_counter()


class Kufar(AbcDataClassScraper):

    @staticmethod
    async def _get_price_usd(price_usd: str) -> int:
        price_usd = price_usd[:-2] if len(price_usd) > 2 else 0

        return price_usd

    @staticmethod
    async def _get_price_br(price_br: str) -> int:
        price_br = price_br[:-2] if len(price_br) > 2 else 0

        return price_br

    @staticmethod
    async def _get_properties_ad(properties: str) -> dict:
        properties_car = dict.fromkeys(('Марка', 'Модель', 'Год', 'Тип двигателя',
                                        'Объем, л', 'Область', 'Город / Район'), 'НЕ указано')

        for prop in properties:
            if prop['pl'] in properties_car:
                properties_car[prop['pl']] = prop['vl']

        return properties_car

    @staticmethod
    async def _get_date_ad(date: str) -> datetime:

        date_obj = datetime.datetime.strptime(date.replace('T', ' ')[:-1], '%Y-%m-%d %H:%M:%S') + \
                   datetime.timedelta(hours=3)

        return date_obj

    async def _get_ads(self, session: aiohttp.ClientSession, page_url: str) -> None | NoReturn:
        try:
            async with session.get(url=page_url, headers=self.HEADERS) as response:
                cars = await response.json()
                await asyncio.sleep(1)
                print(response.url)

                for car in cars['ads']:

                    date_ad = await self._get_date_ad(car['list_time'])
                    if date_ad > self.tracking_date:
                        properties = await self._get_properties_ad(car['ad_parameters'])

                        price_br = await self._get_price_br(car['price_byn'])
                        price_usd = await self._get_price_usd(car['price_usd'])

                        link = car['ad_link']
                        print(properties, price_br, price_usd, link, sep='\n')
                        print('-----------------------------------------')
                    else:
                        continue
        except aiohttp.ClientConnectionError as cce:
            raise cce
        except Exception as ex:
            raise ex

    async def _create_task(self) -> None | NoReturn:
        url = f'https://api.kufar.by/search-api/v1/search/rendered-paginated?' \
              f'prc=r%3A{self.price_min}%2C{self.price_max}'

        try:
            async with aiohttp.ClientSession() as session:
                tasks = []

                for type_car in self.type_cars:
                    type_car_url = url + f'&cat={type_car}'

                    response = await session.get(url=type_car_url, params=self.params, headers=self.HEADERS)
                    await asyncio.sleep(1)

                    response_json = await response.json()

                    page_tokens = response_json['pagination']['pages']

                    for page in page_tokens:
                        if not page['token']:
                            page_url = str(response.url)
                        else:
                            page_url = str(response.url) + '&cursor=' + str(page['token'][:-2]) + '%3D%3D'

                        task = asyncio.create_task(self._get_ads(session=session, page_url=page_url))
                        tasks.append(task)

                await asyncio.gather(*tasks)
        except aiohttp.ClientConnectionError as cce:
            raise cce
        except Exception as ex:
            raise ex


kufar = Kufar()
asyncio.run(kufar._create_task())

finish = time.perf_counter()

print(finish - start)