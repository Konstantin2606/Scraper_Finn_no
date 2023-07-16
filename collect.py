from bs4 import BeautifulSoup as bs
import requests as rq
import time

#collecting data def
def collect(url, param, options): 
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
    except:
        print('Something wrong.')
    return alt
