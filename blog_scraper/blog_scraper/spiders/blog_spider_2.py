# -*- coding: utf-8 -*-
"""A spider to scrape title from my blog

Go to the scrapy project root (i.e. the folder with scrapy.cfg) and run:
scrapy crawl blog2 -o titles2.json

To understand how to scrape a website, use the Scrapy shell
scrapy shell 'http://giacomodebidda.com'

See also blog_spider1.py (it should be a worse implementation)

The JSON files created with the blog1 spider and the blog2 spider should contain
the same data, but maybe they are not identical because the blog2 spider yields
a python dict, which could arrange the key-value pairs in a different way every
time the spider runs. To check that the JSON files are the same, run:
diff titles1.json titles2.json
"""
import scrapy


class MyBlogSpider(scrapy.Spider):
    name = 'blog2'
    start_urls = ['http://www.giacomodebidda.com']

    def parse(self, response):
        # CSS selector...
        # for selector in response.css(".post>h1"):
        # or XPath selector
        for selector in response.xpath("//div[@class='post']/h1"):
            yield {
                'title': selector.xpath("a/text()").extract_first(),
                'link': selector.xpath("a/@href").extract_first(),
            }
