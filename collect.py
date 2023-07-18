from bs4 import BeautifulSoup as bs
import requests as rq
from fake_useragent import UserAgent as UA
import time


#collecting data def
def collect(categ, url, param, options):
    
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
                one = []
                one.append(i.find("a").text) #name
                one.append(i.find('span', {'class':'text-12 text-gray-500'}).text) #from
                one.append(i.find('span', {'class':'text-14 text-gray-500'}).text) #adress
                #trying to find square_metre, price
                sqm_pr = i.find('div', {'class': 'mt-16 flex justify-between sm:mt-8 sm:block space-x-12 font-bold whitespace-nowrap'})
                if not sqm_pr:
                    sqm_pr = i.find('div', {'class': 'col-span-2 mt-16 flex justify-between sm:mt-4 sm:block space-x-12 font-bold whitespace-nowrap'})
                if sqm_pr: #square_metre, price
                    for spr in sqm_pr.find_all('span'): 
                        one.append(spr.text)
                #trying to find price_desc, r_type_amount
                desq_type = i.find('div', {'class': 'text-12 text-gray-500 flex flex-col mt-4 sm:block sm:mt-8'})
                if not desq_type:
                    desq_type = i.find('div', {'class': 'text-12 text-gray-500 flex flex-col mt-4 sm:block'})
                if desq_type: #price_desc, r_type_amount
                    for am in desq_type.find_all('span'):
                        if am.text != ' ∙ ':
                            one.append(am.text)
                visning = i.find('span', {'class':'inline-block px-8 py-4 text-12 border border-bluegray-300 rounded-full'})
                if visning:
                    one.append(visning.text) #Visning
                one.append(i.find('a', {'class': 'sf-search-ad-link link link--dark hover:no-underline'})['href']) #link
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
