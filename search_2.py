# -*- coding: utf-8 -*-
import json
import csv
from downloader import Downloader
import mongo_cache

CSV_FILE = 'countries.csv'
URL = 'http://example.webscraping.com/ajax/search.json?page=0' \
      '&page_size=1000&search_term=.'


def main():
    writer = csv.writer(open(CSV_FILE, 'w'))
    downloader = Downloader(cache=mongo_cache.MongoCache())
    html = downloader(URL)
    ajax = json.loads(html)
    for record in ajax['records']:
        writer.writerow([record['country']])
    print('Records written in {}'.format(CSV_FILE))


if __name__ == '__main__':
    main()
