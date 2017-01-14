# -*- coding: utf-8 -*-
"""Database cache with MongoDB to avoid re-downloading web pages with a crawler.

When we use a crawler for the first time the cache is empty, so all the web
pages are downloaded normally and then added to the cache.
When we already downloaded a web page successfully, the crawler will extract it
from this database cache, so it should complete the task faster.

Requirements
------------
    MongoDB installed
        https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
    pymongo installed
        pip install pymongo
    mongod running
        mongod -dbpath . (foreground process)
        service mongod start (background daemon process)

See Also
--------
    https://docs.mongodb.com/manual/tutorial/manage-mongodb-processes/
"""
import pickle
import zlib
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from bson.binary import Binary
from link_crawler import link_crawler


class MongoCache(object):

    def __init__(self, client=None, expires=timedelta(days=30)):
        """Create a MongoCache object.

        A MoncoCache object is a wrapper around MongoDB to cache downloads.

        Parameters
        ----------
        client : None
            mongo database client
        expires : timedelta
            amount of time before a cache entry is considered expired
        """
        # if a client object is not passed, try connecting to mongodb at the
        # default localhost port
        self.client = MongoClient('localhost',
                                  27017) if client is None else client
        # create collection to store cached webpages, which is the equivalent of
        # a table in a relational database
        self.db = self.client.cache

        try:
            self.db.webpage.create_index(
                'timestamp', expireAfterSeconds=expires.total_seconds())
        except OperationFailure as e:
            print(e)

    def __contains__(self, url):
        try:
            self[url]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, url):
        """Load value at this URL
        """
        record = self.db.webpage.find_one({'_id': url})
        if record:
            # return record['result']
            return pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        """Save value for this URL"""
        # record = {'result': result, 'timestamp': datetime.utcnow()}
        record = {'result': Binary(zlib.compress(pickle.dumps(result))),
                  'timestamp': datetime.utcnow()}
        self.db.webpage.update({'_id': url}, {'$set': record}, upsert=True)

    def clear(self):
        self.db.webpage.drop()

if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/', '/(index|view)',
                 cache=MongoCache())
