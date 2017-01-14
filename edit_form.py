# -*- coding: utf-8 -*-
import requests
import pprint
import login_form
from urllib.parse import urlencode
from robobrowser import RoboBrowser

COUNTRY_URL = 'http://example.webscraping.com/edit/United-Kingdom-239'


def edit_country():
    response = login_form.login_cookies()
    country_html = response.text
    data = login_form.parse_form(country_html)
    pprint.pprint(data)
    print('Population before: ' + data['population'])
    data['population'] = int(data['population']) + 1
    encoded_data = urlencode(data)
    req = requests.get(COUNTRY_URL, data=encoded_data)
    country_html = req.text
    data = login_form.parse_form(country_html)
    print('Population after:', data['population'])


def robobrowser_edit():
    """Use robobrowser to increment population"""

    # login
    br = RoboBrowser(history=True)
    br.open(login_form.LOGIN_URL)
    form = br.get_form(action='#')
    print('form before {}'.format(form))
    form['email'].value = login_form.LOGIN_EMAIL
    form['password'].value = login_form.LOGIN_PASSWORD
    print('form after {}'.format(form))
    br.submit_form(form)

    # edit country
    br.open(COUNTRY_URL)
    form = br.get_forms()[0]
    print('Population before:', form['population'].value)
    form['population'].value = str(int(form['population'].value) + 1)
    br.submit_form(form)

    # check population increased
    br.open(COUNTRY_URL)
    form = br.get_forms()[0]
    print('Population after:', form['population'].value)


if __name__ == '__main__':
    # edit_country()  # not working because of the functions in login_form
    robobrowser_edit()
