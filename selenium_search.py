# -*- coding: utf-8 -*-
"""Perform an automated search with Selenium.

If you need to install chromedriver in Ubuntu or need to know its path:
http://askubuntu.com/questions/539498/where-does-chromedriver-install-to
Another way to know where to find the chromedriver:
dpkg -L chromium-chromedriver

The standalone ChromeDriver binary (which is different than the Chrome browser
binary) must be either in your path or available in the webdriver.chrome.driver
environment variable.
http://stackoverflow.com/a/8259152

The geckodriver (Firefox) must be installed in a different way
http://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu
If you follow the instructions, the driver will be locatead at:
/usr/local/bin/geckodriver
"""
import os
from selenium import webdriver


def main():
    chromedriver = '/usr/lib/chromium-browser/chromedriver'
    os.environ['webdriver.chrome.driver'] = chromedriver
    driver = webdriver.Chrome(chromedriver)

    # or...
    # driver = webdriver.Firefox()

    driver.get('http://example.webscraping.com/search')
    driver.find_element_by_id('search_term').send_keys('.')
    driver.execute_script("document.getElementById('page_size').options[1].text = '1000';")
    driver.find_element_by_id('search').click()
    driver.implicitly_wait(10)  # not working in Firefox?
    links = driver.find_elements_by_css_selector('#results a')
    countries = [link.text for link in links]
    driver.close()
    print(countries)


if __name__ == '__main__':
    main()
