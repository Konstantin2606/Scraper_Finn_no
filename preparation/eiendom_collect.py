import requests as rq
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent as UA
import json



#proxy changes
options = {'proxy': {}} #your proxy

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

def coll_e(options):
    #connect
    url = 'https://www.finn.no/realestate/browse.html'
    side = connect(url, opt=options)

    #collecting and cleaning 'eiendom' types 
    eiendom = side.find_all('li', {'class', 'link--dark'})
    eiendom = dict(map(lambda x: ((x.text).strip().split(' (')[0], x.find('a')['href'].split('?')[0]), eiendom))

    if 'Hotellovernatting' in eiendom: #don't need information about hotells
        del eiendom['Hotellovernatting']
    if 'Bolig til salgs i utlandet' in eiendom: #don't need information from other countries
        del eiendom['Bolig til salgs i utlandet']

    #or (information may not be relevant)
    eiendom_old = {'Bolig til salgs': 'https://www.finn.no/realestate/homes/search.html',
     'Nye boliger': 'https://www.finn.no/realestate/newbuildings/search.html',
     'Tomter': 'https://www.finn.no/realestate/plots/search.html',
     'Fritidsbolig til salgs': 'https://www.finn.no/realestate/leisuresale/search.html',
     'Fritidstomter': 'https://www.finn.no/realestate/leisureplots/search.html',
     'Bolig til leie': 'https://www.finn.no/realestate/lettings/search.html',
     'Hjerterom - Bolig til leie': 'https://www.finn.no/realestate/lettings/search.html',
     'Bolig ønskes leid': 'https://www.finn.no/realestate/wanted/search.html',
     'Næringseiendom til salgs': 'https://www.finn.no/realestate/businesssale/search.html',
     'Næringseiendom til leie': 'https://www.finn.no/realestate/businessrent/search.html',
     'Næringstomter': 'https://www.finn.no/realestate/businessplots/search.html',
     'Bedrifter til salgs': 'https://www.finn.no/realestate/companyforsale/search.html',
     'Feriehus og hytter til leie': 'https://www.finn.no/reise/feriehus-hytteutleie/resultat/',
     'Nye boliger, kommer for salg': 'https://www.finn.no/realestate/newbuildings/search.html'}

    #saving
    with open("category_link.json", "w") as file:
        json.dump(eiendom, file,  ensure_ascii=False)
