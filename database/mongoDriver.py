import pymongo
import concurrent.futures
from getCardDict import cardDict 

client = pymongo.MongoClient('mongodb://localhost:27017')
cfvDB = client['cfvDB']
Cards = cfvDB['Cards']

def process_card(card):
    try:
        print(card)
        data = cardDict(card)
        query = {'ID': data['ID']}
        new_values = {"$set": data}
        Cards.update_one(query, new_values, upsert=True)
    except Exception as e:
        print(f"Error processing card {card}: {str(e)}")
        with open('database\missingcardss.txt', 'a+', encoding='utf-8') as file:
            file.write(card + ' ' + str(e) + '\n')

def cardDatabase():
    with open ('database\cardnames.txt', 'r', encoding='utf-8') as file:
        card_list = file.readlines()
        cards = [card.strip().replace('?', '%3F') for card in card_list]
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(process_card, cards)

if __name__ == "__main__":
    cardDatabase()