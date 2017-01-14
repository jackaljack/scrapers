# -*- coding: utf-8 -*-
import requests


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
