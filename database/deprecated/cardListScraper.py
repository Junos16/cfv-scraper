import re
import requests
from bs4 import BeautifulSoup

def getCardList(category):
    print(category)
    quote_page = 'https://cardfight.fandom.com/wiki/'

    response = requests.get(url = quote_page + category)
    soup = BeautifulSoup(response.content, 'html.parser')
    names = []
    
    span = soup.find_all('span', id = re.compile('^Grade'))
    tables = [x.parent.find_next('table') for x in span]

    for table in tables:
        rows = table.findChildren('tr')
        for row in rows:
            td = row.find_next('td')
            names.append(td.text.replace(' ', '_'))    

    return(names)