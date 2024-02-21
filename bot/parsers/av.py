import requests


class Av:

    def __init__(self, price_min: int = 0, price_max: int = 500, type_car: str = 'cars') -> None:
        self.price_min = price_min
        self.price_max = price_max
        self.type_car = type_car

    def __repr__(self):
        return f'{self.__class__.__name__}(min_price={self.min_price}, max_price={self.max_price},' \
               f' type_car="{self.type_car}")'

    def get_url(self):
        params = {'price_usd[min]': self.price_min, 'price_usd[max]': self.price_max, 'sort': 4}

        url = f'https://api.av.by/offer-types/{self.type_car}/filters/main/init?'

        request = requests.get(url=url, params=params)
        response = request.url

        return response

av = Av()

print(av.get_url())



