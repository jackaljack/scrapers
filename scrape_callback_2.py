# -*- coding: utf-8 -*-
import csv
import re
import lxml.html
from link_crawler import link_crawler


CSV_FILE = 'countries.csv'
FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent',
          'tld', 'currency_code', 'currency_name', 'phone',
          'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')


class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open(CSV_FILE, 'w'))
        self.fields = FIELDS
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search('/view/', url):
            tree = lxml.html.fromstring(html)
            row = list()
            for field in self.fields:
                row.append(tree.cssselect(
                    'table > tr#places_{}__row > td.w2p_fw'.format(field))[
                               0].text_content())
            print('URL match!  --> scraping and writing to {}'.format(CSV_FILE))
            self.writer.writerow(row)


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/', link_regex='/view',
                 scrape_callback=ScrapeCallback())
