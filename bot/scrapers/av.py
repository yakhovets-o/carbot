import datetime

import asyncio
import aiohttp

from typing import NoReturn

from bot.scrapers.abc_data_class_scraper import AbcDataClassScraper as DataClass
from bot.db.orm_query import OrmQuery


class Av(DataClass):

    @staticmethod
    async def _get_date_ad(date: str) -> datetime:
        date_obj = datetime.datetime.strptime(date.replace('T', ' ').split('+')[0],
                                              '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=3)
        return date_obj

    @staticmethod
    async def _get_properties_ad(properties: list) -> dict:
        properties_car = dict.fromkeys(('brand', 'model', 'year', 'engine_capacity',
                                        'engine_type', 'condition'), 'Не указано')

        for prop in properties:
            if prop['name'] in properties_car:
                properties_car[prop['name']] = prop['value']
        return properties_car

    async def _get_ads(self, session: aiohttp.ClientSession, page_url: str) -> None | NoReturn:
        tracking_date = datetime.datetime.strptime(self.tracking_date, '%Y-%m-%d %H:%M:%S')
        try:
            async with session.get(url=page_url, headers=self.HEADERS) as response:
                ads = await response.json()
                await asyncio.sleep(1)

                for ad in ads['adverts']:
                    date_ad = await self._get_date_ad(ad['refreshedAt'])
                    if date_ad > tracking_date:
                        properties = await self._get_properties_ad(ad['properties'])
                        properties |= {'region': ad['locationName'], 'city': ad['shortLocationName'],
                                       'price_br': ad['price']['byn']['amount'], 'date_time_ad': date_ad,
                                       'price_usd': ad['price']['usd']['amount'], 'link': ad['publicUrl'],
                                       'tg_id': self.tg_id}

                        # av table
                        await OrmQuery.add_av_ads(data=properties)

                    else:
                        continue
        except aiohttp.ClientConnectionError as cce:
            raise cce
        except Exception as ex:
            raise ex

    async def create_task(self) -> None | NoReturn:
        try:
            async with aiohttp.ClientSession() as session:
                tasks = []
                for type_car in self.type_cars:
                    type_car_url = f'https://api.av.by/offer-types/{type_car}/filters/main/init?'
                    response = await session.get(url=type_car_url, params=self.params, headers=self.HEADERS)
                    await asyncio.sleep(1)

                    response_json = await response.json()
                    url = response.url

                    count_pages = int(response_json['pageCount'])
                    for page in range(1, count_pages + 1):
                        page_url = str(url) + f'&page={page}'

                        task = asyncio.create_task(self._get_ads(session=session, page_url=page_url))
                        tasks.append(task)

                await asyncio.gather(*tasks)
        except aiohttp.ClientConnectionError as cce:
            raise cce
        except Exception as ex:
            raise ex
