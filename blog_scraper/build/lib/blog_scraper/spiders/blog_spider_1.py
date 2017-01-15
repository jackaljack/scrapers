# -*- coding: utf-8 -*-
"""A spider to scrape title from my blog

Go to the scrapy project root (i.e. the folder with scrapy.cfg) and run:
scrapy crawl blog1 -o titles1.json

To understand how to scrape a website, use the Scrapy shell
scrapy shell 'http://giacomodebidda.com'

See also blog_spider2.py (it should be a better implementation)

The JSON files created with the blog1 spider and the blog2 spider should contain
the same data, but maybe they are not identical because the blog2 spider yields
a python dict, which could arrange the key-value pairs in a different way every
time the spider runs. To check that the JSON files are the same, run:
diff titles1.json titles2.json
"""
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ..items import BlogScraperItem


class MyBlogSpider(BaseSpider):
    name = 'blog1'
    start_urls = ['http://www.giacomodebidda.com']

    def parse(self, response):
        selector = Selector(response)
        # CSS selector
        # blog_titles = selector.css(".post>h1")
        # or XPath selector
        blog_titles = selector.xpath("//div[@class='post']/h1")
        selections = []

        for data in blog_titles:
            selection = BlogScraperItem()
            selection['title'] = data.xpath("a/text()").extract_first()
            selection['link'] = data.xpath("a/@href").extract_first()
            selections.append(selection)

        return selections
