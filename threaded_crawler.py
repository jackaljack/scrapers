# -*- coding: utf-8 -*-
import time
import threading
from urllib import parse
from scrape_callback_1 import scrape_callback as scrape
from downloader import Downloader
from mongo_cache import MongoCache

SLEEP_TIME = 1


def threaded_crawler(seed_url, delay=5, cache=None, scrape_callback=None,
                     user_agent='wswp', proxies=None, num_retries=1,
                     max_threads=10, timeout=60):
    """Crawl a website in multiple threads.

    Keep creating threads while there are URLs to crawl until the maximum number
    of threads is reached.

    Parameters
    ----------
    seed_url : str
    delay : int
    cache : MongoCache, or None
    scrape_callback : function, or None
    user_agent : str
    proxies : None
    num_retries : int
    max_threads : int
    timeout : int
    """
    # the queue of URL's that still need to be crawled
    # crawl_queue = Queue.deque([seed_url])
    crawl_queue = [seed_url]
    seen = set([seed_url])
    downloader = Downloader(cache=cache, delay=delay, user_agent=user_agent,
                            proxies=proxies, num_retries=num_retries,
                            timeout=timeout)

    def process_queue():
        while True:
            try:
                url = crawl_queue.pop()
            except IndexError:
                # crawl queue is empty
                break
            else:
                html = downloader(url)
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e:
                        print('Error in callback for: {}: {}'.format(url, e))
                    else:
                        for link in links:
                            link = normalize(seed_url, link)
                            # check whether already crawled this link
                            if link not in seen:
                                seen.add(link)
                                # add this new link to queue
                                crawl_queue.append(link)

    # wait for all download threads to finish
    threads = list()
    while threads or crawl_queue:
        for thread in threads:
            if not thread.is_alive():
                # remove the stopped threads
                threads.remove(thread)
        while len(threads) < max_threads and crawl_queue:
            thread = threading.Thread(target=process_queue)
            # set this thread as a daemon thread, so the main thread can exit
            # when receives ctrl+c
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        # sleep temporarily so CPU can focus execution on other threads
        time.sleep(SLEEP_TIME)


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain.

    Parameters
    ----------
    seed_url
    link

    Returns
    -------

    """
    link, _ = parse.urldefrag(link)  # remove hash to avoid duplicates
    return parse.urljoin(seed_url, link)

if __name__ == '__main__':
    threaded_crawler('http://example.webscraping.com', delay=0, num_retries=1)
