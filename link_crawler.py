# -*- coding: utf-8 -*-
import re
from urllib import parse, robotparser
from downloader import Downloader


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain.

    Parameters
    ----------
    seed_url : str
    link : str

    Returns
    -------
    str
    """
    link, _ = parse.urldefrag(link)  # remove hash to avoid duplicates
    return parse.urljoin(seed_url, link)


def same_domain(url1, url2):
    """Check whether both URL belong to same domain or not.

    Parameters
    ----------
    url1, url2 : str
        The two URL to check

    Returns
    -------
    bool
        True if the two URL belong to the same domain. False otherwise.
    """
    return parse.urlparse(url1).netloc == parse.urlparse(url2).netloc


def get_robots(url):
    """Initialize robots parser for this domain.

    Parameters
    ----------
    url : str

    Returns
    -------
    rp : RobotFileParser
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(parse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def get_links(html):
    """Extract all links from the webpage.

    Parameters
    ----------
    html : str
        text of the html page

    Returns
    -------
    list
        links from the html page
    """
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1,
                 user_agent='wswp', proxies=None, num_retries=1,
                 scrape_callback=None, cache=None):
    """Crawl from the given seed URL following links matched by link_regex.

    Parameters
    ----------
    seed_url : str
    link_regex : str
    delay : int
    max_depth : int
    max_urls : int
    user_agent : str
    proxies : NoneType
    num_retries : int
    scrape_callback : NoneType
    cache : NoneType

    Returns
    -------

    """
    # the queue of URL's that still need to be crawled
    crawl_queue = [seed_url]
    # the URL's that have been seen and at what depth
    seen = {seed_url: 0}
    # track how many URL's have been downloaded
    num_urls = 0
    rp = get_robots(seed_url)
    downloader = Downloader(delay=delay, user_agent=user_agent,
                            proxies=proxies, num_retries=num_retries,
                            cache=cache)

    while crawl_queue:
        url = crawl_queue.pop()
        depth = seen[url]
        if rp.can_fetch(user_agent, url):
            html = downloader(url)
            links = list()
            if scrape_callback:
                links.extend(scrape_callback(url, html) or [])

            if depth != max_depth:
                if link_regex:
                    links.extend(link for link in get_links(html)
                                 if re.match(link_regex, link))

                for link in links:
                    link = normalize(seed_url, link)
                    # check whether already crawled this link
                    if link not in seen:
                        seen[link] = depth + 1
                        # check link is within same domain
                        if same_domain(seed_url, link):
                            # success! add this new link to queue
                            crawl_queue.append(link)

            # check whether have reached downloaded maximum
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print('Blocked by robots.txt:', url)


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0,
                 num_retries=1, user_agent='BadCrawler')
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0,
                 num_retries=1, max_depth=1, user_agent='GoodCrawler')
