import requests
import re
import logging
from urllib.parse import urlparse, parse_qsl, urlencode

logger = logging.getLogger('tbapi')


def nice_url(url):
    KEEPED_QUERY = ['id', ]
    url_tuple = urlparse(url)
    qs = parse_qsl(url_tuple.query)
    new_qs = urlencode(list(filter(lambda k_v: k_v[0] in KEEPED_QUERY, qs)))
    return url_tuple._replace(scheme='http', query=new_qs).geturl()


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

        Unit:
            RMB
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
            (item['name'], nice_url(item['url']))
            for item in self.json['listItem'][:limit]
        ]

    def unit_price_tuple(self):
        '''
        Get information about unit price.

        Return:
            (`min_price`, `max_price`, `mean_price`)

        Unit:
            RMB/500g
        '''
        prices = []
        for item in self.json['listItem']:
            p = re.search('(\d+)[g克]', item['title'], re.IGNORECASE)
            if p is not None:
                prices.append(float(item['price'])*500/float(p.group(1)))
                continue

            p = re.search('(\d+)(kg|千克)', item['title'], re.IGNORECASE)
            if p is not None:
                prices.append(float(item['price'])*0.5/float(p.group(1)))
                continue

            p = re.search('(\d+)斤', item['title'], re.IGNORECASE)
            if p is not None:
                prices.append(float(item['price'])/float(p.group(1)))
                continue
            logger.debug(
                'No reasonable data in title: {}'.format(item['title']))
        return tuple(
            func(prices) for func in (min, max, lambda l: sum(l) / len(l)))


if __name__ == '__main__':
    import pprint
    tb_api = TB_Searcher('tuna')
    pprint.pprint(tb_api.unit_price_tuple())
