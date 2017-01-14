# -*- coding: utf-8 -*-
import json
from downloader import Downloader
import mongo_cache

TXT_FILE = 'countries.txt'
TEMPLATE_URL = 'http://example.webscraping.com/ajax/search.json?page={}' \
               '&page_size=10&search_term={}'


def main(string):
    countries = set()
    downloader = Downloader(cache=mongo_cache.MongoCache())

    for letter in string.lower():
        page = 0
        while True:
            html = downloader(TEMPLATE_URL.format(page, letter))
            try:
                ajax = json.loads(html)
            except ValueError as e:
                print(e)
                ajax = None
            else:
                for record in ajax['records']:
                    countries.add(record['country'])
            page += 1
            if ajax is None or page >= ajax['num_pages']:
                break

    with open(TXT_FILE, 'w') as f:
        f.write('\n'.join(sorted(countries)))
    print('Records written in {}'.format(TXT_FILE))


if __name__ == '__main__':
    main('y')
