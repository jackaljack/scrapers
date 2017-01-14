# -*- coding: utf-8 -*-
"""Show some information useful to crawl a website.

Usually a website defines a robots.txt file to let robots know any restrictions
about crawling it. The URL of the website sitemap should also be defined in
robots.txt. More information about the robots.txt protocol is available at:
http://www.robotstxt.org

To understand if we can fetch a given URL with a given user agent we have to
parse the robots.txt file. For this task we can use urllib.robotparser.

Example:
    $ python info_about_website http://example.webscraping.com/ -w -r -m
    $ python info_about_website http://google.com/ -r

See Also
    Interesting project to make a sitemap from a website
    https://github.com/c4software/python-sitemap

TODO: it would be nice to show some information about how a website is built.
There is a python module called builtwith for this task, but it's not compatible
with python 3.x. Fork the project and make it available for python 3.x.

TODO: estimate size/links of a website
"""
import argparse
import requests
import whois  # it's called python-whois


def parse_args():
    parser = argparse.ArgumentParser(
        description='Show some information useful to crawl a website')
    parser.add_argument('url', type=str, help='website URL')
    parser.add_argument('-w', '--whois', action='store_true', help='show WHOIS')
    parser.add_argument('-r', '--robots', action='store_true',
                        help='show robots.txt')
    parser.add_argument('-m', '--sitemap', action='store_true',
                        help='show sitemap.xml')
    # parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],
    #                     help="increase output verbosity")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    url = args.url
    print('URL\n{}'.format(url))
    if args.whois:
        print('\nWHOIS\n{}'.format(whois.whois(args.url)))
    if args.robots:
        req = requests.get('{}robots.txt'.format(url))
        print('\nROBOTS.TXT\n{}'.format(req.text))
    if args.sitemap:
        req = requests.get('{}sitemap.xml'.format(url))
        print('\nSITEMAP\n{}'.format(req.text))
