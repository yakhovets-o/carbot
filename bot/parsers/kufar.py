import time

import requests
import datetime


class Kufar:
    cookies = {
        'lang': 'ru',
        'rl_session': 'RudderEncrypt^%^3AU2FsdGVkX19iNSUxN2B5FdpIR1k5DokUZ4CPk3lmBeiAtVqIWry8nYOAkRenCKgmgqfFD4PR1H8McHVsIFwqxVQiAZx2B3G6n1m2do3Qpw7LvGtxYjcghBKLKMEF^%^2Brremdh^%^2BjPFtr5MpTmNb7VD97g^%^3D^%^3D',
        'rl_user_id': 'RudderEncrypt^%^3AU2FsdGVkX18NrRjjmC4UxdoFfK3ryAtJuZ^%^2B4X2ta1XM^%^3D',
        'rl_trait': 'RudderEncrypt^%^3AU2FsdGVkX1^%^2BquOSPOXlqEGCJZd3nAs^%^2FcauprwQpZLuE^%^3D',
        'rl_group_id': 'RudderEncrypt^%^3AU2FsdGVkX19C35R7IWj6VsINHdrfIkWPtlQaaX5XDCc^%^3D',
        'rl_group_trait': 'RudderEncrypt^%^3AU2FsdGVkX1^%^2FcwXCADxva3E2I7idnBJJsC6zvpgP1KRA^%^3D',
        'rl_anonymous_id': 'RudderEncrypt^%^3AU2FsdGVkX1^%^2FDZaNdAAW8BtWlAfPYS27Pimw1Q7yox3NXxNZ6D5BApx^%^2FGKQrjafBmipNXTBpxlhIBal9ARKXoNQ^%^3D^%^3D',
        'rl_page_init_referrer': 'RudderEncrypt^%^3AU2FsdGVkX1^%^2FBz^%^2FyZ2m8uvvocKht037Dsv0uvDDy9NCN02G0lqMC^%^2BEUKvzRju40bs',
        'rl_page_init_referring_domain': 'RudderEncrypt^%^3AU2FsdGVkX189FjPjp8epCB3WBKetTBl5Xy^%^2BYU3T7QpCPxFBAI7R7ZLZSP1gW5X^%^2Fp',
        '_ga': 'GA1.2.214778382.1689607879',
        'kuf_agr': '{^%^22advertisements^%^22:true^%^2C^%^22statistic^%^22:true^%^2C^%^22mindbox^%^22:true}',
        'fullscreen_cookie': '1',
        '_ga_QTFZM0D0BE': 'GS1.1.1708680384.28.1.1708680455.60.0.0',
        '_hjSessionUser_2040951': 'eyJpZCI6ImFlNGE4YTk0LTc0NTQtNTY3Yy1hNTkzLWFlODJmYTNiMzE1MCIsImNyZWF0ZWQiOjE2ODk2MDc4ODc0NTQsImV4aXN0aW5nIjp0cnVlfQ==',
        'tmr_lvid': 'c0b96724852b44284334629446be9d1a',
        'tmr_lvidTS': '1689607887498',
        '__gads': 'ID=b6e08b6691b2d272:T=1689607867:RT=1708680280:S=ALNI_MZKt-llxOSeOKaXBa06o7bCegWzzw',
        '__gpi': 'UID=00000c6a5b4c38bb:T=1689607867:RT=1708680280:S=ALNI_MbIkSN_GZFVcs3OZWnxCBGwigaWvw',
        '_ga_WLP2F7MG5H': 'GS1.1.1708631841.19.0.1708631841.60.0.0',
        'kuf_SA_subscribe_user_attention': '1',
        'kuf_oauth_nonce': 'f1f6e607-412f-4092-9f28-64d108f55209',
        'kuf_auth_last_login_type': 'email',
        'cto_bundle': 'JA4ZxV82UzN2Zml4dWxtNzY3R0Y5V1FYakZQQyUyQnNmcXhYVTVhb0FhenNlR09jcVE1MENHckJnQzE0byUyRlpNbWhvMTJSbHhOJTJCeCUyRmdyUXo0WDg0JTJCWGpheWd0ZDhMdG1nWWg0eFZraVIwYyUyRjRZZmtCaTNnMGNsT2l3N05CVjlHQiUyRnBlamd2ekkzNyUyRm5PJTJGNWxYYmRPS3RRJTJGYTh5ZyUzRCUzRA',
        'default_ca': '5',
        'default_m': '102',
        'kufar-test-variant-web-ab-recommendations-banners-experiment': '59f72c15-e1c5-44fb-845c-ce22d3fd1367__0',
        'web_push_banner_listings': '3',
        '_gcl_au': '1.1.219935340.1708451392',
        'kuf_SA_KufarHotelsPromo': '1',
        '_gid': 'GA1.2.1440580756.1708451409',
        '_ga_4DSS63YZ2R': 'GS1.1.1708451469.1.1.1708455228.0.0.0',
        '_ym_uid': '1708451475461142917',
        '_ym_d': '1708451475',
        'kufar_cart_id': '82aaf93d-df7e-42f7-8726-356ac8d374b9',
        'kufar-mb-check-name_2654975': '1',
        '_fbp': 'fb.1.1708451481902.709355691',
        'supportOnlineTalkID': 'xcTZEomsGyEa68iuEb3SO062gSPaIwOt',
        'kuf_auth_last_logins': '^[{^%^22accountId^%^22:^%^222654975^%^22^%^2C^%^22name^%^22:^%^22LeGo^%^22^%^2C^%^22avatar_url^%^22:^%^22https://content.kufar.by/prc_thumbs/64/6416958872.jpg^%^22^%^2C^%^22profile_image^%^22:^%^226416958872^%^22^%^2C^%^22login^%^22:^%^22yakhovetso^@gmail.com^%^22^%^2C^%^22loginType^%^22:^%^22google^%^22}^]',
        'k_jwt': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InYyMCIsInNjaHYiOiIyIiwidHlwIjoiSldUIn0.eyJhaWQiOiIyNTIwMzY4IiwiY2FkIjpmYWxzZSwiZGlkIjoiNzVjNzU0Y2E1NWJhYmY0NjJmOTAxZmNmMGZhMDdjYTciLCJleHAiOjE3NDA1OTIyMjYsImlhdCI6MTcwODQ1MTQyNiwianRpIjoiMjUyMDM2ODpiUmhTSzNSZiIsInB0ciI6ZmFsc2UsInR5cCI6InVzZXIifQ.1yMmxKzRm0u7RMdZNQXx1zkaDWrdANTqUydHxIt9S3k',
        'session': '1',
        'session_id': 'mc1xed3a4181755f15712c676853c55770e50ecd8bcb',
        'kufar-mb-check-name_2520368': '1',
        'web_push_banner_auto': '3',
        '_ga_D1TYH5F4Z4': 'GS1.1.1708631840.4.0.1708631840.60.0.0',
        '__eoi': 'ID=70f14c065ea256a5:T=1708451755:RT=1708680280:S=AA-Afja9LoqGaT07QxzHemxbDn71',
        '_ym_isad': '2',
        'mindboxDeviceUUID': '3473b177-ee14-4699-a228-e67eefd774ca',
        'directCrm-session': '^%^7B^%^22deviceGuid^%^22^%^3A^%^223473b177-ee14-4699-a228-e67eefd774ca^%^22^%^7D',
        'web_push_banner_realty': '3',
        '_ga_SW9X2V65F0': 'GS1.1.1708635179.2.0.1708635179.0.0.0',
        '_hjSessionUser_1751529': 'eyJpZCI6IjYwNjM0Zjg3LWFkNzQtNTI5MC04MWIzLWZkZWQ1ZjY1ODdiYSIsImNyZWF0ZWQiOjE3MDg2MzE5Mzc3MzQsImV4aXN0aW5nIjp0cnVlfQ==',
        '_tt_enable_cookie': '1',
        '_ttp': '1o0fFsyH3P3kbwXiYZLVKejL7-B',
        'default_ya': '246',
        'kuf_SA_compare-button': '1',
        '_hjSession_2040951': 'eyJpZCI6IjBhNzhlZmM4LTFiZjItNDkwYi1hZjAzLTJjMGNmNDk0MWY4NSIsImMiOjE3MDg2ODAzODkwODAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=',
        '_ym_visorc': 'b',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        # 'Cookie': 'lang=ru; rl_session=RudderEncrypt^%^3AU2FsdGVkX19iNSUxN2B5FdpIR1k5DokUZ4CPk3lmBeiAtVqIWry8nYOAkRenCKgmgqfFD4PR1H8McHVsIFwqxVQiAZx2B3G6n1m2do3Qpw7LvGtxYjcghBKLKMEF^%^2Brremdh^%^2BjPFtr5MpTmNb7VD97g^%^3D^%^3D; rl_user_id=RudderEncrypt^%^3AU2FsdGVkX18NrRjjmC4UxdoFfK3ryAtJuZ^%^2B4X2ta1XM^%^3D; rl_trait=RudderEncrypt^%^3AU2FsdGVkX1^%^2BquOSPOXlqEGCJZd3nAs^%^2FcauprwQpZLuE^%^3D; rl_group_id=RudderEncrypt^%^3AU2FsdGVkX19C35R7IWj6VsINHdrfIkWPtlQaaX5XDCc^%^3D; rl_group_trait=RudderEncrypt^%^3AU2FsdGVkX1^%^2FcwXCADxva3E2I7idnBJJsC6zvpgP1KRA^%^3D; rl_anonymous_id=RudderEncrypt^%^3AU2FsdGVkX1^%^2FDZaNdAAW8BtWlAfPYS27Pimw1Q7yox3NXxNZ6D5BApx^%^2FGKQrjafBmipNXTBpxlhIBal9ARKXoNQ^%^3D^%^3D; rl_page_init_referrer=RudderEncrypt^%^3AU2FsdGVkX1^%^2FBz^%^2FyZ2m8uvvocKht037Dsv0uvDDy9NCN02G0lqMC^%^2BEUKvzRju40bs; rl_page_init_referring_domain=RudderEncrypt^%^3AU2FsdGVkX189FjPjp8epCB3WBKetTBl5Xy^%^2BYU3T7QpCPxFBAI7R7ZLZSP1gW5X^%^2Fp; _ga=GA1.2.214778382.1689607879; kuf_agr={^%^22advertisements^%^22:true^%^2C^%^22statistic^%^22:true^%^2C^%^22mindbox^%^22:true}; fullscreen_cookie=1; _ga_QTFZM0D0BE=GS1.1.1708680384.28.1.1708680455.60.0.0; _hjSessionUser_2040951=eyJpZCI6ImFlNGE4YTk0LTc0NTQtNTY3Yy1hNTkzLWFlODJmYTNiMzE1MCIsImNyZWF0ZWQiOjE2ODk2MDc4ODc0NTQsImV4aXN0aW5nIjp0cnVlfQ==; tmr_lvid=c0b96724852b44284334629446be9d1a; tmr_lvidTS=1689607887498; __gads=ID=b6e08b6691b2d272:T=1689607867:RT=1708680280:S=ALNI_MZKt-llxOSeOKaXBa06o7bCegWzzw; __gpi=UID=00000c6a5b4c38bb:T=1689607867:RT=1708680280:S=ALNI_MbIkSN_GZFVcs3OZWnxCBGwigaWvw; _ga_WLP2F7MG5H=GS1.1.1708631841.19.0.1708631841.60.0.0; kuf_SA_subscribe_user_attention=1; kuf_oauth_nonce=f1f6e607-412f-4092-9f28-64d108f55209; kuf_auth_last_login_type=email; cto_bundle=JA4ZxV82UzN2Zml4dWxtNzY3R0Y5V1FYakZQQyUyQnNmcXhYVTVhb0FhenNlR09jcVE1MENHckJnQzE0byUyRlpNbWhvMTJSbHhOJTJCeCUyRmdyUXo0WDg0JTJCWGpheWd0ZDhMdG1nWWg0eFZraVIwYyUyRjRZZmtCaTNnMGNsT2l3N05CVjlHQiUyRnBlamd2ekkzNyUyRm5PJTJGNWxYYmRPS3RRJTJGYTh5ZyUzRCUzRA; default_ca=5; default_m=102; kufar-test-variant-web-ab-recommendations-banners-experiment=59f72c15-e1c5-44fb-845c-ce22d3fd1367__0; web_push_banner_listings=3; _gcl_au=1.1.219935340.1708451392; kuf_SA_KufarHotelsPromo=1; _gid=GA1.2.1440580756.1708451409; _ga_4DSS63YZ2R=GS1.1.1708451469.1.1.1708455228.0.0.0; _ym_uid=1708451475461142917; _ym_d=1708451475; kufar_cart_id=82aaf93d-df7e-42f7-8726-356ac8d374b9; kufar-mb-check-name_2654975=1; _fbp=fb.1.1708451481902.709355691; supportOnlineTalkID=xcTZEomsGyEa68iuEb3SO062gSPaIwOt; kuf_auth_last_logins=^[{^%^22accountId^%^22:^%^222654975^%^22^%^2C^%^22name^%^22:^%^22LeGo^%^22^%^2C^%^22avatar_url^%^22:^%^22https://content.kufar.by/prc_thumbs/64/6416958872.jpg^%^22^%^2C^%^22profile_image^%^22:^%^226416958872^%^22^%^2C^%^22login^%^22:^%^22yakhovetso^@gmail.com^%^22^%^2C^%^22loginType^%^22:^%^22google^%^22}^]; k_jwt=eyJhbGciOiJIUzI1NiIsImtpZCI6InYyMCIsInNjaHYiOiIyIiwidHlwIjoiSldUIn0.eyJhaWQiOiIyNTIwMzY4IiwiY2FkIjpmYWxzZSwiZGlkIjoiNzVjNzU0Y2E1NWJhYmY0NjJmOTAxZmNmMGZhMDdjYTciLCJleHAiOjE3NDA1OTIyMjYsImlhdCI6MTcwODQ1MTQyNiwianRpIjoiMjUyMDM2ODpiUmhTSzNSZiIsInB0ciI6ZmFsc2UsInR5cCI6InVzZXIifQ.1yMmxKzRm0u7RMdZNQXx1zkaDWrdANTqUydHxIt9S3k; session=1; session_id=mc1xed3a4181755f15712c676853c55770e50ecd8bcb; kufar-mb-check-name_2520368=1; web_push_banner_auto=3; _ga_D1TYH5F4Z4=GS1.1.1708631840.4.0.1708631840.60.0.0; __eoi=ID=70f14c065ea256a5:T=1708451755:RT=1708680280:S=AA-Afja9LoqGaT07QxzHemxbDn71; _ym_isad=2; mindboxDeviceUUID=3473b177-ee14-4699-a228-e67eefd774ca; directCrm-session=^%^7B^%^22deviceGuid^%^22^%^3A^%^223473b177-ee14-4699-a228-e67eefd774ca^%^22^%^7D; web_push_banner_realty=3; _ga_SW9X2V65F0=GS1.1.1708635179.2.0.1708635179.0.0.0; _hjSessionUser_1751529=eyJpZCI6IjYwNjM0Zjg3LWFkNzQtNTI5MC04MWIzLWZkZWQ1ZjY1ODdiYSIsImNyZWF0ZWQiOjE3MDg2MzE5Mzc3MzQsImV4aXN0aW5nIjp0cnVlfQ==; _tt_enable_cookie=1; _ttp=1o0fFsyH3P3kbwXiYZLVKejL7-B; default_ya=246; kuf_SA_compare-button=1; _hjSession_2040951=eyJpZCI6IjBhNzhlZmM4LTFiZjItNDkwYi1hZjAzLTJjMGNmNDk0MWY4NSIsImMiOjE3MDg2ODAzODkwODAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; _ym_visorc=b',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    type = 'sell'
    sort = 'lst.d'
    lang = 'ru'
    size = 30

    def __init__(self,
                 tg_id: int = 6165,
                 cars: bool = 1,
                 truck_cars: bool = 1,
                 currency: str = 'Br',
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

        self.urls = self.__get_url()

    def __get_url(self):
        self.currency = 'USD' if self.currency == 'Usd' else 'BYR'

        if self.currency == 'BYR':
            self.price_min = self.price_min * 100
            self.price_max = self.price_max * 100

        # 2010 category cars, 2060 category truck cars
        type_cars = {2010 if self.cars else 2060, 2060 if self.truck_cars else 2010}

        params = {'cur': self.currency, 'size': self.size, 'sort': self.sort, 'typ': self.type,
                  'lang': self.lang}

        url = f'https://api.kufar.by/search-api/v1/search/rendered-paginated?prc=r%3A{self.price_min}%2C{self.price_max}'

        cars_url = {}

        for type_car in type_cars:
            params.update(cat=type_car)

            request = requests.get(url=url, params=params, cookies=self.cookies, headers=self.headers)
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

                    url_page = requests.get(url=response + token, cookies=self.cookies, headers=self.headers)
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

    def __get_ads_cars(self, cars_urls: list) -> tuple | requests.exceptions.RequestException:

        try:
            for url in cars_urls:

                request = requests.get(url=url, cookies=self.cookies, headers=self.headers)

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
        cars_urls = self.urls.get(2010)

        return self.__get_ads_cars(cars_urls=cars_urls)

    def get_truck_cars(self):
        truck_cars_urls = self.urls.get(2060)

        return self.__get_ads_cars(cars_urls=truck_cars_urls)


kufar = Kufar()
print(kufar.get_cars())

print(kufar.get_truck_cars())
