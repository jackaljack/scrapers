import requests
import itertools


def download(url, user_agent='wswp', num_retries=2):
    print('Downloading:', url)
    headers = {'User-agent': user_agent}
    r = requests.get(url, headers=headers)
    try:
        html = r.text
    except Exception as e:
        # TODO: see which exception to catch
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                return download(url, user_agent, num_retries-1)
    return html


def crawl_by_iteration():
    """Iterate through all pages of the website and download them all.

    We can use this crawler when the web server ignores the slug and only use
    the ID to match with relevant records in the database.
    """
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view/-{}'.format(page)
        html = download(url)
        if html is None:
            break
        else:
            # success - can scrape the result
            pass


if __name__ == '__main__':
    crawl_by_iteration()
