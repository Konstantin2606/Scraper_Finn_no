from base import base
from collect import collect
from connect_site import connect
from cleaning import cleaning
from proxies import proxies
from data_df import data_df
import pandas as pd
from datetime import datetime

#Cleaning def working good, but
#I heve SettingWithCopyWarning problem there, and i didn't solv it yet.
#I'll turn on ignore if it scares you or something.
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

def start():
    options = proxies() #proxies
    
    f = base() #what do you need to collect?
    
    data = collect(*f, options=options) #collecting process
    
    data = data_df(data, f[0]) #columns settings
    
    data = cleaning(data) #cleaning process
    
    #saving to csv
    print('Do you want to save? - yes/no or 1/0')
    for i in range(1, 5):
        ans = input()
        if ans in ('yes', 'y', '1'):
            #naming
            c_datetime = datetime.now()
            f_date = c_datetime.strftime("%Y_%m_%d_%Hh_%Mm_%Ss")
            f = f[0].replace(' ', '_')
            name = f'{f}_{len(result)}_{f_date}rows.csv'
            result.to_csv(f'results/{name}', sep=',', index=False, encoding='utf-8-sig')
            print(f'Saved - filename - {name}')
            break
        elif ans in ('no', 'n', '0'):
            print("Answer - don't")
            break
        else:
            print('-- something wrong, try again --')
    return result
