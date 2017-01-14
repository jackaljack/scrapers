# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import requests
from http import cookiejar
import lxml.html


LOGIN_EMAIL = 'example@webscraping.com'
LOGIN_PASSWORD = 'example'
LOGIN_URL = 'http://example.webscraping.com/user/login'
COUNTRY_URL = 'http://example.webscraping.com/edit/United-Kingdom-239'


def login_basic():
    # can't work
    print('login_basic')
    data = {'email': LOGIN_EMAIL, 'password': LOGIN_PASSWORD}
    encoded_data = urlencode(data)
    req = requests.get(LOGIN_URL, data=encoded_data)
    print(req.url)
    print('Status code: {}\n'.format(req.status_code))
    return req


def login_formkey():
    # can't work
    print('login_formkey')
    req = requests.get(LOGIN_URL)
    html = req.text
    data = parse_form(html)
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urlencode(data)
    req = requests.get(LOGIN_URL, data=encoded_data)
    print(req.url)
    print('Status code: {}\n'.format(req.status_code))
    return req


def login_cookies():
    # TODO: should work but it doesn't. Fix it
    print('login_cookies')
    cj = cookiejar.CookieJar()
    req = requests.get(LOGIN_URL, cookies=cj)
    html = req.text
    data = parse_form(html)
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urlencode(data)
    req = requests.get(LOGIN_URL, data=encoded_data)
    print(req.url)
    print('Status code: {}\n'.format(req.status_code))
    return req


def parse_form(html):
    """extract all input properties from the form"""
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


def main():
    login_basic()
    login_formkey()
    login_cookies()


if __name__ == '__main__':
    main()
