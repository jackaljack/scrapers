# -*- coding: utf-8 -*-
import requests
import re


URL = 'http://example.webscraping.com/view/United-Kingdom-239'


def scrape(html):
    area = re.findall(
        '<tr id="places_area__row">.*?<td\s*class=["\']w2p_fw["\']>(.*?)</td>',
        html)[0]
    return area


if __name__ == '__main__':
    req = requests.get(URL)
    print(scrape(req.text))
