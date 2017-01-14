# -*- coding: utf-8 -*-
import requests
from urllib import parse
import random
import time
from datetime import datetime
import socket

DEFAULT_AGENT = 'wswp'  # wswp = web scraping with python
DEFAULT_DELAY = 5
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 60


class Downloader:
    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT,
                 proxies=None, num_retries=DEFAULT_RETRIES,
                 timeout=DEFAULT_TIMEOUT, opener=None, cache=None):
        """Create a Downloader object.

        Parameters
        ----------
        delay : int
        user_agent : str
        proxies : None
        num_retries : int
        timeout : int
        opener : None
        cache : MongoCache, or None
        """
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.opener = opener
        self.cache = cache

    def __call__(self, url):
        """Make the Downloader object callable.

        Parameters
        ----------
        url : str

        Returns
        -------
        str
            html of the web page just downloaded
        """
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # url is not available in cache
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    # server error so ignore result from cache and re-download
                    result = None
        if result is None:
            # result was not loaded from cache so we still need to download
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy=proxy,
                                   num_retries=self.num_retries)
            if self.cache:
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries, data=None):
        """

        Parameters
        ----------
        url : str
        headers : dict
        proxy : None
        num_retries : int
        data : None

        Returns
        -------
        dict
            html (str) and response code (int)
        """
        print('Downloading:', url)
        req = requests.get(url, data=data, headers=headers)
        try:
            html = req.text
        except Exception as e:
            print('Download error: {}'.format(e))
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    # retry 5XX HTTP errors
                    return self._get(url, headers, proxy, num_retries - 1, data)

        return {'html': html, 'code': req.status_code}


class Throttle:

    def __init__(self, delay):
        """Create a Throttle object.

        Throttle downloading by sleeping between requests to same domain.
        Throttle only when a download is made, not when loading from a cache.

        Parameters
        ----------
        delay : int
            amount of delay between downloads for each domain
        """
        self.delay = delay
        self.domains = dict()  # timestamp of when a domain was last accessed

    def wait(self, url):
        """Delay if have accessed this domain recently.

        Parameters
        ----------
        url : str
        """
        domain = parse.urlsplit(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()
