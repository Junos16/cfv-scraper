import requests
from bs4 import BeautifulSoup

quote_page = 'https://cardfight.fandom.com/wiki/'

# add method to get clans according to marker generated https://cardfight.fandom.com/wiki/Template:ClansV
# maybe redo clans with this https://cardfight.fandom.com/wiki/Template:Clans

def markerScraper():
    response = requests.get(url = quote_page + 'Template:ClansV')
    soup = BeautifulSoup(response.content, 'html.parser')

    markers = []

    th = soup.find_all('th', class_ = 'navbox-group')

    for tag in th:
        currentMarker = []

        try:
            markerName = tag.findChild('a').findNext('a').get('title')
            currentMarker.append(markerName)

        except:
            currentMarker.append(tag.text.strip())

        clans = tag.findNext('td').findChildren('a')

        for clan in clans:
            currentMarker.append(clan.text.strip())

        markers.append(currentMarker)

    return(markers)

def clanScraper():
    response = requests.get(url = quote_page + 'clans')
    soup = BeautifulSoup(response.content, 'html.parser')

    header = soup.find('span', id = 'List_of_Clans').parent
    nation_divs = header.find_next_siblings('div')
    clans = []
    nations = [x.text.strip() for x in nation_divs]
    for nation in nation_divs:
        clan_list = [nation.text.strip()]
        clan_list += [x.text.strip() for x in nation.find_next_sibling().findChildren('td')]
        clan_list = [x for x in clan_list if x!='']
        clans.append(clan_list)

    common = ['common']
    no_nation = [None]

    td = soup.find(id = 'Other_Clans').parent.find_next_sibling('table').findChildren('td')
    other_data = [x.text.strip() for x in td]
    for i in range(0, 38, 3):
        clan = other_data[i]
        details = other_data[i+1]

        if any(nation in details for nation in nations):
            for i in range(len(clans)):
                nation_temp = clans[i][0]
                if nation_temp in details:
                    clans[i].append(clan)

        elif 'same' in details:
            nation = [clan]
            clans.append(nation)

        elif 'all' in details:
            common.append(clan)

        else:
            no_nation.append(clan)

    clans.append(common)
    clans.append(no_nation)

    return(clans)

# maybe redo nations with this https://cardfight.fandom.com/wiki/Template:Nations
def nationScraper():
    response = requests.get(url = quote_page + 'Nations')
    soup = BeautifulSoup(response.content, 'html.parser')
    
    nations = []
    
    info = soup.find('div', class_ = 'NavFrame')
    frames = info.findChildren('div', class_ = 'NavFrame')

    for frame in frames:
        content = frame.findChild('div', class_ = 'NavContent')
        temp_nations = [x.text.strip() for x in content.findChildren('a') if x.text.strip() != '']
        nations.append(temp_nations)

    return(nations)