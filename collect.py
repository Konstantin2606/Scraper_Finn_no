from bs4 import BeautifulSoup as bs
import requests as rq
from fake_useragent import UserAgent as UA
import time


#collecting data def
def collect(url, param, options):
    
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
    
    alt = []
    try:
        while True:
            soup = connect(url, params=param, opt=options)
            print('connection successful')
            for i in soup.find_all('article'):
                p = i.find_all('span')
                one = []
                one.append(i.find("a").text)
                for o in p:
                    d = o.text
                    one.append(d)
                one.append(i.find('a')['href'])
                alt.append(one)
            try:
                link = soup.find('nav', {"class": 'pagination u-pb8 u-pt16'}).find_all('a')[-1]['href']
                link = link[1:]
                link = dict(map(lambda x: x.split('='), link.split('&')))
                if link['page'] == param['page']:
                    raise Exception('Last link.')
                else:
                    param = link
                time.sleep(5)
            except:
                print('All is collected!')
                break    
    except Exception as e:
        print(f"Something wrong: {e}")
    return alt
