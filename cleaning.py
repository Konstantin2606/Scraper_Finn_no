import pandas as pd
import numpy as np

#cleaning data def
def cleaning(all_data): #from data_df
    df = all_data.drop_duplicates()
    pd.set_option('display.max_colwidth', None)
    
    #for price
    if 'price' in df.columns:
        try:
            df['price'] = df['price'].str.split('-').str[-1] #clean from '-'
            df['price'] = df['price'].str[:-3] #clean from 'kr'
            df['price'] = df['price'].str.replace('\xa0', '') #clean from '\xa0'
            if df['price'].str.contains('http').sum(): #clean from http
                df = df[~df['price'].str.contains('http')]
                
            #price to int
            try:
                df['price'] = df['price'].map(int)
                if len(df.loc[df['price'] < 100, 'price'])>0: #clean from untrust values
                    df.loc[df['price'] < 100, 'price'] =0
            except:
                print("can't make price int")

        except:
            print('problem with price descr')
    
    #for price_desc
    if 'price_desc' in df.columns:
        try:
            #trying to understend if is something to split
            df_pr = df['price_desc'].str.split(' ∙ ', expand=True) 
            df_pr_count = df_pr.iloc[0].count()#!!!! mistake--------------------------------------!!!!
            
            #if 2 items
            if df_pr_count == 2:
                df[['total_price', 'fellesutg']] = df_pr
                del df['price_desc']

                #fellestung cleaning
                try:
                    # clean from- :, -, kr, \xa0
                    df.loc[:, 'fellesutg'] = df['fellesutg'].str.split(':').str[-1].str.split('-').str[-1].str[:-3].str.replace('\xa0', '')
                    try:
                        df['fellesutg'].fillna(0, inplace=True) #fill None with 0
                        df.loc[:, 'fellesutg'] = df['fellesutg'].map(int) #make int
                    except:
                        print("can't make fellesutg int")
                        
                except:
                    print('problem with fellesutg cleaning')
            
            #if nothing to split, probably it's a total
            if df_pr_count == 1:
                df['total_price'] = df_pr
                del df['price_desc']
            
            #total_price cleaning
            try:
                # clean from- :, -, kr, \xa0
                df.loc[:, 'total_price'] = df['total_price'].str.split(':').str[-1].str.split('-').str[-1].str[:-3].str.replace('\xa0', '')
                try:
                    df['total_price'].fillna(0, inplace=True) #fill None with 0
                    df.loc[:, 'total_price'] = df['total_price'].map(int) #make int
                except:
                    print("can't make total_price int")
                    
            except:
                print('problem with total_price cleaning')
                
        except:
            print('problem with price_desc descr')

    #for r_type_amount
    if 'r_type_amount' in df.columns:
        try:
            #trying to understend if is something to split
            df_am = df['r_type_amount'].str.split(' ∙ ', expand=True)
            df_am_count = df_am.iloc[0].count() #!!!!!!!!!!! --------------- could give a mistake!!!!!!
            
            #if 2 items
            if df_am_count == 2:
                
                if df_am.iloc[:, -1].str.contains('Leilighet|Hus').sum(): #is it type
                    df[['owner?', 'type']] = df_am
                    del df['r_type_amount']
                
                elif df_am.iloc[:, -1].str.isdigit().sum(): #is it rooms amount
                    df[['type', 'rooms_amount']] = df_am
                    del df['r_type_amount']

            
            #if 3 items
            elif df_am_count == 3:
                df[['owner?', 'type', 'rooms_amount']] = df_am
                del df['r_type_amount']

            #clean 'rooms_amount' from str -'rooms' and make int
            if 'rooms_amount' in df.columns:
                df.loc[:, 'rooms_amount'] = df['rooms_amount'].str.split().str[0] #clean from str 'rooms'

                try:
                    df['rooms_amount'].fillna(0, inplace=True) #fill None with 0
                    df.loc[:, 'rooms_amount'] = df['rooms_amount'].map(int) #make int
                except:
                    print("can't make rooms_amount int")

            #more settings - sometimes nessesery
            df.loc[df['type'] == 'Garasje/Parker', ['type']] = 'Garasje/Parkering'
        
        except:
            print('problem with r_type_amount descr')
            
    #for square_metre
    if 'square_metre' in df.columns:
        try:
            if df['square_metre'].str.contains('http').sum(): #clean from http
                df = df[~df['square_metre'].str.contains('http')]
            df['square_metre'] = df['square_metre'].str.split().str[0] #clean from 'm2'
            df['square_metre'] = df['square_metre'].map(int) #make int
        
        except:
            print('problem with square_metre descr')
            
    #for visning
    if 'visning' in df.columns:
        try:
            #is there any links
            html_v = df['visning'].str.contains('http')
            if html_v.sum():
                df.loc[html_v, 'link'] = df.loc[html_v, 'visning']
                df.loc[html_v, 'visning'] = ''
            #clean from str - 'visning'
            df['visning'] = df['visning'].str.split(' - ').str[-1]
            
        except:
            print('problem with visning descr')
    
    return df
