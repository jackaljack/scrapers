# -*- coding: utf-8 -*-
import requests
from io import StringIO
from lxml import etree
from lxml.cssselect import CSSSelector

URL = 'http://example.webscraping.com/view/United-Kingdom-239'


def scrape(html):
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    root = tree.getroot()
    selector = CSSSelector('tr#places_area__row > td.w2p_fw')
    element = selector(root)[0]
    area = element.text
    return area


if __name__ == '__main__':
    req = requests.get(URL)
    print(scrape(req.text))
