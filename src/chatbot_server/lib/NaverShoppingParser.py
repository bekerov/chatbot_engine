#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup


class NaverShoppingParser:
    def __init__(self, query):
        self.naver = {
            'url': 'http://m.shopping.naver.com/search/all.nhn',
            'params': {
                'query': query
            }
        }

    def get(self):
        response = requests.get(**self.naver)
        bs = BeautifulSoup(response.text, 'html.parser')
        result_set = bs.find('ul', attrs={'id': 'grid'})
        items = []
        for item in result_set.find_all('li'):
            if item.find('span', attrs={'class': 'info_tit'}) is not None:
                name = item.find('span', attrs={'class': 'info_tit'}).get_text().strip()
            else:
                continue

            if item.find('span', attrs={'class': 'price'}) is not None:
                price = item.find('span', attrs={'class': 'price'}).get_text().strip()
            else:
                continue

            if item.find('img', attrs={'class': '_productLazyImg'}) is not None:
                image = item.find('img', attrs={'class': '_productLazyImg'}).get('data-original')
            else:
                continue

            if item.find('a', attrs={'class': 'a_link'}) is not None:
                link = item.find('a', attrs={'class': 'a_link'}).get('href')

            items.append({
                'name': name,
                'price': price,
                'image': image,
                'link': link
            })

        return items
