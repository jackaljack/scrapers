# -*- coding: utf-8 -*-
"""Sitemap crawler.

Try to download all web pages listed in sitemap.xml
Keep in mind that sitemap files often cannot be relied on to provide links to
every web page of a website.
"""
import re
from common import download


URL = 'http://example.webscraping.com/sitemap.xml'


def crawl_sitemap():
    """Download the sitemap, extract links by using a regex, download all links.
    """
    sitemap = download(URL)
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    for link in links:
        html = download(link)
        # scrape html here
        # ...


if __name__ == '__main__':
    crawl_sitemap()
