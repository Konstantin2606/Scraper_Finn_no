import requests as rq
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent as UA

#requests and bs4 connect
def connect(url, params={}, opt={"proxy": {}}):
    ua = UA()
    header = {
        'user-agent': ua.random,
        'x-requested-with': 'XMLHttpRequest'}
    proxies = opt['proxy']
    resp = rq.get(url, headers=header, proxies=proxies, params=param, timeout=1)
    resp.encoding = 'utf-8-sig'
    soup = bs(resp.text, 'lxml')
    return soup
