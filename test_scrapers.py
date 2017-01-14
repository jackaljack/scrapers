# -*- coding: utf-8 -*-
import unittest
from mongo_cache import MongoCache
from datetime import timedelta
from time import sleep


class TestMongoCache(unittest.TestCase):

    def setUp(self):
        self.url = 'http://example.webscraping.com'
        self.result = {'html': '...'}

    def test_result_is_not_none(self):
        cache = MongoCache()
        cache.clear()
        self.assertIsNotNone(self.result['html'])

    def test_cache_not_yet_expired(self):
        cache = MongoCache()
        cache[self.url] = self.result
        self.assertIsInstance(cache[self.url], dict)

    @unittest.skip('test_cache_expired skipped: too slow')
    def test_cache_expired(self):
        cache = MongoCache(expires=timedelta())
        # every 60 seconds the cache is purged
        # http://docs.mongodb.org/manual/core/index-ttl/
        cache[self.url] = self.result
        sleep(61)
        with self.assertRaises(KeyError):
            cache[self.url]


if __name__ == '__main__':
    unittest.main()
