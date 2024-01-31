import requests
from bs4 import BeautifulSoup

quote_page = 'https://cardfight.fandom.com/wiki/'

# generalize it to not have to use a key list
# format has issues due to use of icons instead of text, find solution
def getMainInfo(table):
    keyList = ['Name', 'Card Type', 'Grade / Skill', 'Imaginary Gift', 'Power', 'Critical', 'Shield', 
            'Nation', 'Clan', 'Trigger Effect', 'Race', 'Format', 'Illust'] 
    
    mainInfo = {}
    
    for key in keyList:
        if key in table:
            keyIndex = table.index(key)
            value = table[keyIndex+1]
            mainInfo[key] = value
        else:
            mainInfo[key] = None
    
    return mainInfo

def getSets(inputList):
    setList = []

    for item in inputList:
        br_tags = item.find_all('br')
        for br_tag in br_tags:
            br_tag.replace_with(' - ')

    inputList = [x.text.strip() for x in inputList]

    for string in inputList:
        parts = string.split(' - ')

        if len(parts) >= 2:
            for part in parts[1:]:
                setList.append(part)

    return setList

def labelFlavors(flavorList):
    flavorDict = {}
    for string in flavorList:
        parts = string.split(':', 1)
        
        if len(parts) == 2:
            key = parts[0][1:-1]
            value = parts[1].strip()
            flavorDict[key] = value
    
    return flavorDict

def getEffects(tagList):
    effect_list = []
    cur_effect = ''

    for tag in tagList:
        if tag.name == 'br':
            effect_list.append(cur_effect.strip())
            cur_effect = ''
        else:
            text = tag.get_text().strip().replace('\n', '')
            cur_effect += text + ' '
    
    effect_list.append(cur_effect.strip())
    return effect_list

# restrictions don't register properly as it is an image, figure out a solution
def getTourneyStatus(tStatus):
    tourneyStatus = {}
    for i in range(0, len(tStatus), 2):
        tourneyStatus[tStatus[i]] = tStatus[i+1]

    return tourneyStatus

def getCardData(cardName):
    response = requests.get(url = quote_page + cardName)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find(class_ = 'info-main').findChildren('td')
    table = [x.text.strip() for x in table]
    cardData = getMainInfo(table)
    
    sets = soup.find(class_ = 'sets').findChildren('li') 
    cardData['Sets'] = getSets(sets)
    print(cardData['Sets'])

    try:
        flavor = list(soup.find(class_ = 'flavor').find('td').stripped_strings)
        cardData['Flavor Texts'] = labelFlavors(flavor)
    except:
        cardData['Flavor Texts'] = None

    try:
        effects = list(soup.find(class_ = 'effect').find('td'))
        cardData['Effects'] = getEffects(effects)
    except:
        cardData['Effects'] = None
        

    tStatus = soup.find(class_ = 'tourneystatus').findChildren('td')
    tStatus = [x.text.strip() for x in tStatus]
    cardData['Tourney Status'] = getTourneyStatus(tStatus)

    return cardData


getCardData('Absolution_Lion_King,_Mithril_Ezel')