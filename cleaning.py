import pandas as pd
import numpy as np

#cleaning data def
def cleaning(all_data): 
    leie = all_data.drop_duplicates()
    pd.set_option('display.max_colwidth', None)
    leie['price'] = leie['price'].str[:-3]
    leie['price'] = leie['price'].str.replace('\xa0', '')
    recover = leie[~leie['price'].str.isdigit()]
    if len(recover) > 0:
        leie.loc[~leie['price'].str.isdigit(), ['price']] = recover['square_metre']
        leie.loc[~leie['price'].str.isdigit(), ['r_type_amount']] = recover['price']
        leie.loc[~leie['price'].str.isdigit(), ['square_metre']] = '0'
        leie.loc[~leie['price'].str.isdigit(), ['price']] = leie['price'].str[:-3]
        leie.loc[~leie['price'].str.isdigit(), ['price']] = leie['price'].str.replace('\xa0', '')
    leie.loc[0, 'link'] = leie.loc[0, 'trash2']

    leie[['type', 'rooms_amount']] = leie['r_type_amount'].str.split(' ∙ ', expand=True)
    del leie['r_type_amount']

    leie = leie.reindex(('name', 'from', 'address', 'square_metre', 'price', 'type', 'rooms_amount', 'link'), axis=1)
    leie['price'] = leie['price'].map(int)
    leie['square_metre'] = leie['square_metre'].str.split().str[0]
    leie['square_metre'] = leie['square_metre'].map(int)
    leie.loc[leie['type'] == 'Garasje/Parker', ['type']] = 'Garasje/Parkering'

    if len(leie.loc[leie['price'] < 100, 'price'])>0:
        leie.loc[leie['price'] < 100, 'price'] =0
        
    return leie
