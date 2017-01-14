# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


URL = 'http://example.webscraping.com/view/United-Kingdom-239'


def scrape(html):
    soup = BeautifulSoup(html, 'html.parser')  # slower
    # soup = BeautifulSoup(html, 'lxml')  # slightly faster (requires lxml)
    tr = soup.find(attrs={'id':'places_area__row'})
    td = tr.find(attrs={'class':'w2p_fw'})
    area = td.text
    return area

if __name__ == '__main__':
    req = requests.get(URL)
    print(scrape(req.text))
