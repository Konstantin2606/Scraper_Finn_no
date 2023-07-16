import time
import json
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

#proxy changes
options = {'proxy': {}} #your proxy

def coll_cities(options):
    #places collect
    url = 'https://www.finn.no/realestate/homes/search.html'
    with webdriver.Chrome(seleniumwire_options=options) as browser:
        browser.get(url)
        omr = []
        #open all boxes
        clk = [place.click() for place in browser.find_elements(By.XPATH, "//label[contains(@for, 'location')]")]
        #collecting
        for place in browser.find_elements(By.XPATH, "//label[contains(@for, 'location')]"):
            omr.append((place.text, place.get_attribute('for')))
        time.sleep(5)

    #cleaning
    omr = list(map(lambda x: (x[0].split(' (')[0], x[1].split('-')),omr))

    #saving
    omrde = dict(omr)
    with open("omrde.json", "w") as file:
        json.dump(omrde, file,  ensure_ascii=False)
