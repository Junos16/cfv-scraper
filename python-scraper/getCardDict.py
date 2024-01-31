import requests
from bs4 import BeautifulSoup

base_url = 'https://cardfight.fandom.com/wiki/'

# get image links
# griph vartex flavor issue
# fix individual missing cards

def get_main_info(table, card):
    mainInfo = {}

    for i in range(0, len(table), 2):
        key = table[i].text.strip()
        value = table[i+1].text.strip()

        if 'Grade' in key:
            key1, key2 = map(str.strip, key.split('/'))
            if '/' in value:
                values = list(map(str.strip, value.split('/')))
                value1 = int(values[0][5:].strip())
                value2 = values[1:] if len(values) > 2 else values[1]
                mainInfo[key1], mainInfo[key2] = value1, value2
            else:
                mainInfo[key1] = int(value[5:].strip())
        elif key in ['Power', 'Shield', 'Critical']:
            if value not in ['N/A', 'None']:
                value = int(value.replace('+', '').replace(',', ''))
                mainInfo[key] = value
            else:
                mainInfo.pop(key, None)
        elif key == 'Imaginary Gift':
            key = 'Ride'
            try:
                value = table[i+1].findChild('a')['title']
            except:
                value = None
            mainInfo[key] = value    
        else:
            mainInfo[key] = value

    if mainInfo['Format'] != 'Premium':
        add = 'D ' if 'Standard' in mainInfo['Format'] else 'V '
        mainInfo['Format'] = add + mainInfo['Format']
        mainInfo['Format'] = list(map(str.strip, mainInfo['Format'].split('/')))

    response = requests.get(base_url + 'Special:Export/' + card)
    soup = BeautifulSoup(response.content, 'lxml')
    text = soup.find('text').text

    if 'Persona' in text:
        mainInfo['Ride'] = 'Persona'

    mainInfo['ID'] = soup.find('page').findChild('id').text
    mainInfo['Title'] = soup.find('page').findChild('title').text
    mainInfo['Link'] = base_url + card.replace(' ', '_')

    return mainInfo

def get_sets(sets):
    set_dict = {}

    for line in sets:
        br_tags = line.find_all('br')
        for br_tag in br_tags:
            br_tag.replace_with(' - ')
        
        string_list = line.text.split(' - ')
        key, value = string_list[0], string_list[1:]
        set_dict[key] = value
   
    return set_dict

def get_flavor_text(flavor):
    if ':' in flavor:
        flavorDict = {}
        for string in flavor:
            parts = string.split(':', 1)
            
            if len(parts) == 2:
                key = parts[0][1:-1]
                value = parts[1].strip()
                flavorDict[key] = value

        return flavorDict
    else:
        return flavor

def get_effects(effects):
    #print(effects)
    for br_tag in effects.find_all('br'):
        br_tag.replace_with('|||')

    effect_text = effects.get_text()
    #print(effect_text)
    effect_list = [text.strip() for text in effect_text.split('|||')]
    #print(effect_list)
    return effect_list

def get_tourney_status(tStatus):
    keys = [x.text.strip() for x in tStatus[0::2]]
    values = []

    for i in range(0, len(tStatus), 2):
        value = tStatus[i+1]
        #print(value)
        if value.text.strip() != 'Unrestricted':
            format_texts = [x.strip() for x in value.get_text().split('/')]
            restriction_texts = [x['title'] for x in value.findChildren('a')]
            restriction_dict = dict(zip(format_texts, restriction_texts))
            values.append(restriction_dict)
        else:
            values.append(value.text.strip())

    tourneyStatus = dict(zip(keys, values))
    return tourneyStatus

def cardDict(card):
    page = base_url + card
    response = requests.get(page)
    #html = asyncio.run(fetch_page(card))
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find(class_ = 'info-main').findChildren('td')
    #table = [x.text.strip() for x in table]
    data = get_main_info(table, card)
    #print(get_main_info(table))

    try:
        sets = soup.find(class_ = 'sets').findChildren('li') 
        data['Sets'] = get_sets(sets)
        #print(data['Sets'])
    except:
        data['sets'] = None

    try:
        flavor = list(soup.find(class_ = 'flavor').find('td').stripped_strings)
        data['Flavor Texts'] = get_flavor_text(flavor)
        #print(data['Flavor Texts'])
    except:
        data['Flavor Texts'] = None
    
    try:
        effects = soup.find(class_ = 'effect').find('td')
        tabber = soup.find(class_ = 'effect').findChild('div', class_ = 'tabber wds-tabber')

        if tabber:
            keys = [x.text for x in tabber.findChildren('div', class_ = 'wds-tabs__tab-label')]
            value_tags = tabber.findChild(class_ = 'wds-tabs__wrapper with-bottom-border').find_next_siblings('div')
            values = [get_effects(x) for x in value_tags]
            data['Effects'] = dict(zip(keys, values))
        else:
            data['Effects'] = get_effects(effects) 
    except:
        data['Effects'] = None
    
    try:
        tStatus = soup.find(class_ = 'tourneystatus').findChildren('td')
        #tStatus = [x.text.strip() for x in tStatus]
        data['Tourney Status'] = get_tourney_status(tStatus)
        #print(data['Tourney Status'])
    except:
        data['Tourney Status'] = None

    return data

print(cardDict('Sheltered_Heiress,_Spangled'))