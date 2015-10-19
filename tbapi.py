import requests


class TB_Searcher:
    def __init__(self, merchandise):
        self.url = "http://s.m.taobao.com/search"
        self.params = {
            'q': merchandise,
            'search': '提交查找',
            'sst': 1,
            'n': 20,
            'buying': 'buyitnow',
            'm': 'api4h5',
            'abtest': '$abtest',
            'sort': '$abtest',
            'page': '1',
        }
        self.headers = {
            'Host': 's.m.taobao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) '
                          'Gecko/20100101 Firefox/41.0',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        }

    @property
    def json(self):
        if not hasattr(self, '_json'):
            self._json = self._search().json()
        return self._json

    def _search(self):
        return requests.get(self.url, params=self.params, headers=self.headers)

    def price_tuple(self):
        """
        Get information about price.

        Return:
            (`min_price`, `max_price`, `mean_price`)
        """
        prices = [float(item['price']) for item in self.json['listItem']]
        return tuple(
            func(prices) for func in (min, max, lambda l: sum(l) / len(l)))

    def list_items(self, limit=5):
        """
        List title and url of items.

        Return:
            (`title`, `url`)
        """
        return [
            (item['name'], item['url'])
            for item in self.json['listItem'][:limit]
        ]


if __name__ == '__main__':
    import pprint
    tb_api = TB_Searcher('dive into python')
    pprint.pprint(tb_api.list_items())
