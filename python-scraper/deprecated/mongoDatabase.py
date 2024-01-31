import pymongo
import clanNationScraper
import cardListScraper
import database.deprecated.cardDataScraper as cardDataScraper

client = pymongo.MongoClient("mongodb://localhost:27017")
cfvDB = client["cfvDB"] # database creation

# Collections for units
D_Units = cfvDB["D_Units"]
V_Units = cfvDB["V_Units"]
P_Units = cfvDB["P_Units"]

def dUnits():
    nations = clanNationScraper.nationScraper()[0]
    for nation in nations:
        cards = cardListScraper.getCardList(nation)
        for card in cards:
            #key = {'Sets':cardDataScraper.getCardData(card)['Sets']}
            #data = {"$set":cardDataScraper.getCardData(card)}
            #D_Units.update_one(key, data, upsert=True)
            D_Units.insert_one(cardDataScraper.getCardData(card))

def pvUnits():
    vSeries = '_V_Series'
    clans = clanNationScraper.clanScraper()
    temp = []
    for nation in clans:
        if len(nation) == 1:
            temp.append(nation[0])
            temp.append(nation[0] + vSeries)
        else:
            for clan in nation[1:]:
                temp.append(clan)
                temp.append(clan + vSeries)

    for clan in temp:
        try:
            cards = cardListScraper.getCardList(clan)
            if vSeries in clan:
                for card in cards:
                    V_Units.insert_one(cardDataScraper.getCardData(card))
            else:
                for card in cards:
                    P_Units.insert_one(cardDataScraper.getCardData(card))
        except:
            print("doesn't exist")
    
P_Units()