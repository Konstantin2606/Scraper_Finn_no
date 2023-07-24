import pandas as pd
import numpy as np

#cleaning data def
def cleaning(all_data): #from data_df

    # before cleaning
    amount = len(all_data)
    df = all_data.drop_duplicates()
    pd.set_option('display.max_colwidth', None)
    columns = ['name', 'from', 'address']
    print('Result:')
    
    #removing strange birds --------------------------------------------------------------------------------------
    
    if 'visning' in df.columns: #visning
        df['visning'].fillna('0', inplace=True)
        #is there any links
        html_v = df['visning'].str.contains('http')
        if html_v.sum():
            df.loc[html_v, 'link'] = df['visning'][html_v]
            df.loc[html_v, 'visning'] = '0'

    if 'r_type_amount' in df.columns: #r_type_amount
        df['r_type_amount'].fillna('0', inplace=True)
        ow = df['r_type_amount'].str.contains('http|finn') #links in r_type_amount
        df.loc[ow, 'link'] = df['r_type_amount'][ow]
        df.loc[ow, 'r_type_amount'] = '0'
        ow = df['r_type_amount'].str.contains('Visning') #'visning' in r_type_amount
        if 'visning' in df.columns:
            df.loc[ow, 'visning'] = df['r_type_amount'][ow]
        df.loc[ow, 'r_type_amount'] = '0'
        
    if 'price_desc' in df.columns: #price_desc
        df['price_desc'].fillna('0', inplace=True)
        ow = df['price_desc'].str.contains('http|finn') #links in 'price_desc'
        df.loc[ow, 'link'] = df['price_desc'][ow]
        df.loc[ow, 'price_desc'] = '0'
        ow = df['price_desc'].str.contains('Visning') #'visning' in 'price_desc'
        if 'visning' in df.columns:
            df.loc[ow, 'visning'] = df['price_desc'][ow]
        df.loc[ow, 'price_desc'] = '0'
        ow = df['price_desc'].str.contains('kr|0') #'r_type_amount' in 'price_desc'
        if 'r_type_amount' in df.columns:
            df.loc[~ow, 'r_type_amount'] = df['price_desc'][~ow]
        df.loc[~ow, 'price_desc'] = '0'
        
    if 'owner?' in df.columns: #owner? - tomter categ. not so many data(1-2 str), can't use 
        try:
            df['owner?'].fillna('0', inplace=True) #can't work with NaN
            ow = df['owner?'].str.contains('http|finn')
            df.loc[ow, 'link'] = df['owner?'][ow] #changing links columns
            del df['owner?']
        except Exception as e:
            print(f"Can't clean 'owner?' column- {e}")
    
    if 'price' in df.columns:
        df['price'].fillna('0', inplace=True)
        ow = df['price'].str.contains('http|finn') #links in price
        df.loc[ow, 'link'] = df['price'][ow]
        df.loc[ow, 'price'] = '0'
        
        ow = df['price'].str.contains('Totalpris') #price_desc in price
        if 'price_desc' in df.columns: 
            df.loc[ow, 'price_desc'] = df['price'][ow]
        df.loc[ow, 'price'] = '0'
        
        ow = df['price'].str.contains('Visning|Annet fritid') #'visning' in price
        if 'visning' in df.columns:
            df.loc[ow, 'visning'] = df['price'][ow]
        df.loc[ow, 'price'] = '0'
        
        ow = df['price'].str.contains('kr|0') #'r_type_amount' in price
        if 'r_type_amount' in df.columns:
            df.loc[~ow, 'r_type_amount'] = df['price'][~ow]
        df.loc[~ow, 'price'] = '0'
    
    if 'square_metre' in df.columns:
        df['square_metre'].fillna('0', inplace=True)
        ow = df['square_metre'].str.contains('http|finn') #links in 'square_metre'
        df.loc[ow, 'link'] = df['square_metre'][ow]
        df.loc[ow, 'square_metre'] = '0'
        
        ow = df['square_metre'].str.contains('Totalpris')#price_desc in 'square_metre'
        if 'price_desc' in df.columns: 
            df.loc[ow, 'price_desc'] = df['square_metre'][ow]
        df.loc[ow, 'square_metre'] = '0'
        
        ow = df['square_metre'].str.contains('Visning|Annet fritid') #'visning' in 'square_metre'
        if 'visning' in df.columns:
            df.loc[ow, 'visning'] = df['square_metre'][ow]
        df.loc[ow, 'square_metre'] = '0'
        
        ow = df['square_metre'].str.contains('kr') #'price' in 'square_metre'
        if 'price' in df.columns:
            df.loc[ow, 'price'] = df['square_metre'][ow]
        df.loc[ow, 'square_metre'] = '0'

        ow = df['square_metre'].str.contains('m²|0') #'r_type_amount' in 'square_metre'
        if 'r_type_amount' in df.columns:
            df.loc[~ow, 'r_type_amount'] = df['square_metre'][~ow]
        df.loc[~ow, 'square_metre'] = '0'
    
    #main cleaning -----------------------------------------------------------------------------------------------
    
    #for square_metre
    if 'square_metre' in df.columns:
        try:
            df['square_metre'] = df['square_metre'].str.split('-').str[-1] #clean from '-'
            df['square_metre'] = df['square_metre'].str.replace('m²', '') #clean from 'm2'
            df['square_metre'] = df['square_metre'].str.replace('\xa0', '') #clean from '\xa0'
            
            try:
                df['square_metre'] = df['square_metre'].map(int) #make int
            except Exception as e:
                print(f"can't make square_metre int - {e}")
                
        except Exception as e:
            print(f'problem with square_metre descr - {e}')
        
        columns.append('square_metre')
    
    #for price
    if 'price' in df.columns:
        try:
            df['price'] = df['price'].str.split('-').str[-1] #clean from '-'
            df['price'] = df['price'].str.replace('kr', '') #clean from 'kr'
            df['price'] = df['price'].str.replace('\xa0', '') #clean from '\xa0'
                
            #price to int
            try:
                df['price'] = df['price'].map(int)
                if len(df.loc[df['price'] < 100, 'price'])>0: #clean from untrust values
                    df.loc[df['price'] < 100, 'price'] =0
            except:
                print(f"can't make price int - {e}")

        except Exception as e:
            print(f'problem with price descr - {e}')
        
        columns.append('price')
        
    #for price_desc
    if 'price_desc' in df.columns:
        try:
            #trying to understend if is something to split
            df_pr = df['price_desc'].str.split(' ∙ ', expand=True) 
            df_pr_count = len(df_pr.columns)
            #if 2 items
            if df_pr_count == 2:
                df[['total_price', 'fellesutg']] = df_pr
                del df['price_desc']

                #fellestung cleaning
                try:
                    # clean from- :, -, kr, \xa0
                    df.loc[:, 'fellesutg'] = df['fellesutg'].str.split(':').str[-1].str.split('-').str[-1].str.replace('kr', '')
                    df.loc[:, 'fellesutg'] = df['fellesutg'].str.replace(r'^\s*$|^\xa0$', '0', regex=True).str.replace('\xa0', '')
                    try:
                        df['fellesutg'].fillna(0, inplace=True) #fill None with 0
                        df.loc[:, 'fellesutg'] = df['fellesutg'].map(int) #make int
                    except Exception as e:
                        print(f"can't make fellesutg int - {e}")
                        
                except Exception as e:
                    print(f'problem with fellesutg cleaning - {e}')
                
                columns.extend(['total_price', 'fellesutg'])
                
            #if nothing to split, probably it's a total
            if df_pr_count == 1:
                df['total_price'] = df_pr
                del df['price_desc']
                columns.append('total_price')
            #total_price cleaning
            try:
                # clean from- :, -, kr, \xa0
                df.loc[:, 'total_price'] = df['total_price'].str.split(':').str[-1].str.split('-').str[-1].str.replace('kr', '')
                df.loc[:, 'total_price'] = df['total_price'].str.replace(r'^\s*$|^\xa0$', '0', regex=True).str.replace('\xa0', '')
                try:
                    df['total_price'].fillna('0', inplace=True) #fill None with 0
                    df.loc[:, 'total_price'] = df['total_price'].map(int) #make int
                except Exception as e:
                    print(f"can't make total_price int - {e}")
                    
            except Exception as e:
                print(f'problem with total_price cleaning - {e}')
            
        except Exception as e:
            print(f'problem with price_desc descr - {e}')
            columns.append('price_desc')
            
    #for r_type_amount
    if 'r_type_amount' in df.columns:
        
        try:
            #trying to understend if is something to split
            df_am = df['r_type_amount'].str.split(' ∙ ', expand=True)
            df_am_count = len(df_am.columns)
            
            #if 1 item
            if df_am_count == 1:
                df.rename(columns={'r_type_amount': 'type'}, inplace=True)
                columns.append('type')
                
            #if 2 items
            elif df_am_count == 2:

                if df_am.iloc[:, 0].str.contains('Eier').sum(): #is there owner
                    df[['owner?', 'type']] = df_am
                    del df['r_type_amount']
                    columns.extend(['owner?', 'type'])
                    
                elif df_am.iloc[:, -1].str.split().str[0].str.isdigit().sum(): #is there rooms amount
                    df[['type', 'rooms_amount']] = df_am
                    del df['r_type_amount']
                    columns.extend(['type', 'rooms_amount'])
                    
            #if 3 items
            elif df_am_count == 3:
                df[['owner?', 'type', 'rooms_amount']] = df_am
                del df['r_type_amount']
                columns.extend(['owner?', 'type', 'rooms_amount'])

            #clean 'rooms_amount' from str -'rooms' and make int
            if 'rooms_amount' in df.columns:
                df.loc[:, 'rooms_amount'] = df['rooms_amount'].str.split().str[0] #clean from str 'rooms'

                try:
                    df['rooms_amount'].fillna('0', inplace=True) #fill None with 0
                    df.loc[:, 'rooms_amount'] = df['rooms_amount'].map(int) #make int
                except:
                    print("can't make rooms_amount int")
            
            if 'type' in df.columns:
                ow = df['type'].str.contains('Annet fritid')
                if ow.sum() and 'visning' in df.columns:
                    df.loc[ow, 'visning'] = df['type'][ow] 
                    df.loc[ow, 'type'] = '0'
                #more settings - sometimes nessesery
                df.loc[df['type'] == 'Garasje/Parker', ['type']] = 'Garasje/Parkering'
        
        except Exception as e:
            print(f'problem with r_type_amount descr - {e}')
            columns.append('r_type_amount')
    
    #for visning
    if 'visning' in df.columns:
        try:
            #clean from str - 'visning'
            df['visning'] = df['visning'].str.split(' - ').str[-1]
        except Exception as e:
            print(f'problem with visning descr - {e}')
        
        columns.append('visning')
    
    #sort columns ------------------------------------------------------------------------------------------------
    try:
        if df.columns[0] == 0:
            raise Exception("something wrong with columns names...")
        columns.append('link')
        df = df.reindex(columns, axis=1)
    except Exception as e:
        print(f'problem with columns sort - {e}')
    
    print(f'\n-- {amount - len(df)} -- str delited, if there is still a problem, try to clean in manually') # after cleaning
    return df
