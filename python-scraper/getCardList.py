import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp

async def process_page(url, card_list, forbidden_keywords, loop):
    response = await loop.run_in_executor(None, lambda: requests.get(url))
    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', class_='category-page__members-wrapper')
    for div in divs:
        list_items = div.find_all('li')
        for item in list_items:
            card_name = item.text.strip()
            if not any(keyword in card_name for keyword in forbidden_keywords) and card_name != '':
                card_list.append(card_name)
                print(card_name)

async def get_card_list(loop):
    base_url = 'https://cardfight.fandom.com'
    initial_url = base_url + '/wiki/Category:Cards'
    card_list = []
    forbidden_keywords = ['Category:', 'Gallery:', 'Trivia:', 'Errata:', 'Tips:', 'Rulings:', 'Lores:', '(ZERO)', 'User:', '_Gallery', 'User_blog:']

    async with aiohttp.ClientSession() as session:
        while initial_url:
            await process_page(initial_url, card_list, forbidden_keywords,loop)
            response = await loop.run_in_executor(None, lambda: requests.get(initial_url))
            soup = BeautifulSoup(response.content, 'html.parser')
            next_tag = soup.find('a', class_='category-page__pagination-next wds-button wds-is-secondary')
            if next_tag:
                initial_url = next_tag['href']
            else:
                initial_url = None

    with open("database/cardnames.txt", 'w', encoding='utf-8') as file:
        for card_name in sorted(card_list):
            file.write(card_name.replace(' ', '_') + '\n')

    return sorted(card_list)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_card_list(loop))