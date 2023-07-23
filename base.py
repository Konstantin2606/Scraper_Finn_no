import json

#what do you need to scrap
def base():
    with open('preparation/category_link.json', "r") as file: #file with all links (from finn.no)
        data = json.load(file)
    v = dict(enumerate(data.keys(), 1))
    param = ''
    
    #wich category
    print('Сhoose a category:', *(map(lambda x: f'{x[0]}) {x[1]}', v.items())), sep='\n', end='\n(pick number)\n')
    for tr in range(1, 6):
        try:
            chose_categ = input()
            if chose_categ.isdigit():
                chose_categ = v[int(chose_categ)]
            url = data[chose_categ]
            break
        except:
            print('Something wrong, try again.')

    #choose cities or city with radius
    print('Choose a search method:\n1 - "cities"\n2 - "city with radius"\n(pick number)')
    for tr in range(1, 6):
        chose = input()
        if chose in ('1', '2', 'All'):
            break
        else:
            print('Something wrong, try again.')
    
    #if All - secret, because can make a time error, only for small category
    if chose == 'All':
        param = 'page=1&sort=PUBLISHED_DESC'
    
    #if cities
    if chose == '1':
        with open('preparation/omrde.json', "r") as file: #file with cities (from finn.no)
            data = json.load(file)
            
    #with cities
        print('Choose the area\city(use comma and one space between if there is more than one)')
        for tr in range(1, 6):
            try:
                chose = input().title().split(', ')
                cit = []
                for c in chose:
                    if c in data:
                        cit.append('='.join(data[c]))
                print(f'Accepted {len(cit)} cities out of {len(chose)}')
                if len(cit) == 0:
                    raise Error
                break
            except Exception as e:
                print('Something wrong, try again. - {e}')
        #all param
        param = f'{"&".join(cit)}&page=1&sort=PUBLISHED_DESC'
    
    #if one city with radius
    elif chose == '2':
        with open('preparation/no.json', "r") as file: #file with cities (https://simplemaps.com/data/no-cities)
            data = json.load(file)
            data = dict(map(lambda x: (x["city"], (x["lat"], x["lng"])),data))
            
    #wich city + radius
        print('Choose the area and radius(from 200 to 100000 meter) (use one space between)')
        for tr in (1, 6):
            try:
                chose = input().split()
                chose = (chose[0].title(), int(chose[1]))
                if 200 < chose[1] <100000:
                    if chose[0] in data:
                        break
                    print('city fail')
                print('radius fail')
            except Exception as e:
                print('Something wrong, try again. - {e}')
                
        #all param
        param = (('geoLocationName', chose[0]),
            ('lat', data[chose[0]][0]),
            ('lon', data[chose[0]][1]),
            ('radius', f'{chose[1]}'),
            ('sort', 'PUBLISHED_DESC'),
            ('page', '1'))
        param = '&'.join(map(lambda x: f'{x[0]}={x[1]}', param))
    
    #base parametr 
    data = (chose_categ, url, param)
    return data
