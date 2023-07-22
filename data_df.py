import pandas as pd
import numpy as np

#make columns data def
def data_df(data, categ): 
    try:
        if categ in ('Bolig til salgs', 'Nye boliger', 'Fritidsbolig til salgs'):
            try:
                columns = ('name', 'from', 'address', 'square_metre', 'price', 'price_desc', 'r_type_amount', 'visning', 'link')
                df = pd.DataFrame(data, columns=columns)
            except: #if have not visning
                columns = ('name', 'from', 'address', 'square_metre', 'price', 'price_desc', 'r_type_amount', 'link')
                df = pd.DataFrame(data, columns=columns)
                
        elif categ in ('Fritidstomter', ):
            try:
                columns = ('name', 'from', 'address', 'square_metre', 'price', 'price_desc', 'visning', 'link')
                df = pd.DataFrame(data, columns=columns)
            except: #if have not visning
                columns = ('name', 'from', 'address', 'square_metre', 'price', 'price_desc', 'link')
                df = pd.DataFrame(data, columns=columns)

        elif categ in ('Tomter', 'Næringstomter'):
            try:
                columns = ('name', 'from', 'address', 'square_metre', 'price', 'price_desc', 'link')
                df = pd.DataFrame(data, columns=columns)
            except: #if have 'owner?'
                columns = ('name', 'from', 'address', 'square_metre', 'price', 'price_desc', 'owner?', 'link')
                df = pd.DataFrame(data, columns=columns)

        elif categ in ('Bolig til leie', 'Hjerterom - Bolig til leie', 'Næringseiendom til leie', ):
            columns = ('name', 'from', 'address', 'square_metre', 'price', 'r_type_amount', 'link')
            df = pd.DataFrame(data, columns=columns)

        elif categ in ('Næringseiendom til salgs', ):
            columns = ('name', 'from', 'address', 'square_metre', 'price', 'price_desc', 'r_type_amount', 'link')
            df = pd.DataFrame(data, columns=columns)
        elif categ in ('Bedrifter til salgs', ):
            columns = ('name', 'from', 'address', 'price', 'price_desc', 'link')
            df = pd.DataFrame(data, columns=columns)
        return df
    except:
        df = pd.DataFrame(data)
        return df
