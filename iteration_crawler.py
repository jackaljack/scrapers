# -*- coding: utf-8 -*-
import itertools
from common import download


def crawl_by_iteration():
    """Iterate through all pages of the website and download them all.

    We can use this crawler when the web server ignores the slug and only use
    the ID to match with relevant records in the database.
    """
    # maximum number of consecutive download errors allowed
    max_errors = 5
    # current number of consecutive download errors
    num_errors = 0
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view/-{}'.format(page)
        html = download(url)
        if html is None:
            # received an error trying to download this webpage
            num_errors += 1
            if num_errors == max_errors:
                # reached maximum number of
                # consecutive errors so exit
                break
        else:
            # success - can scrape the result
            # ...
            num_errors = 0


if __name__ == '__main__':
    crawl_by_iteration()
