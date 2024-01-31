import deprecated.clanNationScraper as clanNationScraper
from getpass import getpass
from mysql.connector import connect

def updateNationTable():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Nations (
            name VARCHAR(100),
            chakrabarthi_era BOOL,
            PRIMARY KEY(name, chakrabarthi_era)    
        )
    """
    cursor.execute(create_table_query)
    cfvDB.commit()
    
    nations = [(name, 1) for name in clanNationScraper.nationScraper()[0]] + [(name, 0) for name in clanNationScraper.nationScraper()[1]]
    
    insert_record_query = """
    INSERT INTO Nations
    (name, chakrabarthi_era)
    values(%s, %s)    
    """
    cursor.executemany(insert_record_query, nations)
    cfvDB.commit()

def updateClanTable():
    """create_table_query = """
    #CREATE TABLE IF NOT EXISTS Clans (
     #       name VARCHAR(100),
      #      marker VARCHAR(50),
       #     nation VARCHAR(100),
        #    PRIMARY KEY(name, marker, nation)    
        #)
    """
    cursor.execute(create_table_query)
    cfvDB.commit()"""
    
    markers = clanNationScraper.markerScraper()
    clans = clanNationScraper.clanScraper()

    clan_to_marker = {}
    for i in range(len(clans)):
        nation = clans[i][0]
        for clan in clans[i][1:]:
            for marker_list in markers:
                if clan in marker_list:
                    marker = marker_list[0]
                    break
            clan_to_marker[clan] = marker

    # Create the new list of records
    records = []

    for i in range(len(clans)):
        nation = clans[i][0]
        if nation == 'common':
            for j in range(len(clans)):
                if clans[j][0] != 'none':
                    for clan in clans[j][1:]:
                        records.append((clan, clan_to_marker[clan], clans[j][0]))
        else:
            for clan in clans[i][1:]:
                records.append((clan, clan_to_marker[clan], nation))

    print(records)
    """
    insert_record_query = 
    """
    #INSERT INTO Nations
    #(name, marker, nation)
    #values(%s, %s, %s)    
    """
    cursor.executemany(insert_record_query, records)
    cfvDB.commit()
    """

"""
def updateMarkerTable():

def updateNormalUnits():

def updateTriggerUnits():

def updateStrides():

def updateGGuardians():

def updateTokens():

def updateOrders():

def updateRestriction():

def updateChoiceRetriction():

def updateSets():

"""
    
database_name = 'cfvDB'

cfvDB = connect(
    host = "localhost",
    user = input("Enter username: "),
    password = getpass("Enter password: "),
    database = database_name
)

cursor = cfvDB.cursor(buffered=True)
updateClanTable()

