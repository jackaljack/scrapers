# -*- coding: utf-8 -*-
"""A spider to scrape quotes from the website quotes.toscrape.com (from the
Scrapy docs)

Run this spider using the following command in the scrapy project root (i.e. the
folder with scrapy.cfg):
scrapy crawl quotes

If you want to save the output:
scrapy crawl quotes -o quotes.json

You can also provide command line arguments. These arguments will be passed to
the Spider’s __init__ method and will become spider attributes by default.
scrapy crawl quotes -o quotes-humor.json -a tag=humor
"""
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
