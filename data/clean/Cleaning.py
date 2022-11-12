# The aim of this program is to clean the data and prepare it for the analysis

# ../dirty/mtr_lines_and_stations.csv

"""
Line Code,Direction,Station Code,Station ID,Chinese Name,English Name,Sequence
"""

# ../dirty/mtr_lines_fares.csv

"""
SRC_Station_Name,SRC_STATION_ID,DEST_STATION_NAME,DEST_STATION_ID,OCT_ADT_FARE,OCT_STD_FARE,SINGLE_ADT_FARE,OCT_CON_CHILD_FARE,OCT_CON_ELDERLY_FARE,OCT_CON_PWD_FARE,SINGLE_CON_CHILD_FARE,SINGLE_CON_ELDERLY_FARE
"""


# LineInfo.json 
"""
{

    "AEL" : "Airport Express",
    "DRL" : "Disneyland Resort Line",
    "EAL" : "East Rail Line",
    "ISL" : "Island Line",
    "KTL" : "Kwun Tong Line",
    "TML" : "Tuen Ma Line",
    "TCL" : "Tung Chung Line",
    "TKL" : "Tseung Kwan O Line",
    "SIL" : "South Island Line",
    "TWL" : "Tsuen Wan Line"
}
"""

# The url of mtr map website
# https://www.mtr.com.hk/ch/customer/jp/index.php?
# &oType=HRStation
# &oValue=20
# &dType=HRStation
# &dValue=74
# The "cost" is in <span class="time">44 分鐘</span>

# Expected Result:

"""
{
        "name" : "Lo Wu",
        "connections" : [
            {
                "name" : "Sheung Shui",
                "cost" : 6,
                "fromline" : "Tung Chung Line",
            }
        ],
        "line" : ["Tung Chung Line"],
        "line_code" : "ERL",
        "id" : 76,
        "code" : "LOW", 
        "Chinese Name" : "羅湖"
    },
"""


import json
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bs4
import random

base_url = "https://www.mtr.com.hk/share/customer/jp/api/HRRoutes/?lang=C&"
option = Options()
option.add_argument("--headless")
option.add_argument("--no-sandbox")
option.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=option)

def clean_data():
    # Read in the data
    with open(os.path.join('..', 'clean', 'mtr_lines_and_stations.csv')) as f:
        lines = f.readlines()
    with open(os.path.join('..', 'dirty', 'mtr_lines_fares.csv')) as f:
        fares = f.readlines()
    with open(os.path.join('..', 'clean', 'LineInfo.json')) as f:
        line_info = json.load(f)

    # Clean the data
    stations = []
    for line in lines[1:]:
        line = line.strip().split(',')
        station = {
            'name' : line[5],
            'connections' : [],
            'line' : [line_info[line[0]]],
            'line_code' : [line[0]],
            'id' : int(line[3]),
            'code' : line[2],
            'Chinese Name' : line[4],
            'sequence' : int(line[6])
        }
        stations.append(station)
    
    # Add connections by looking at the sequence in the csv file
    for station in stations:
        for other_station in stations:
            if station['id'] == other_station['id'] or station['line_code'] != other_station['line_code']:
                continue

            if abs(station['sequence'] - other_station['sequence']) == 1:

                url = base_url + "o=" + str(station['id']) + "&d=" + str(other_station['id']) 
                driver.get(url)
                soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
                # get the json data from <pre> tag
                text = soup.find('pre').text
                # turn the text in dictionary
                text = json.loads(text)
                cost = text['routes'][0]['path'][1]['time']
                print( station['name'], " -> " , other_station['name'], " --- " , cost)
                station['connections'].append({
                    'name' : other_station['name'],
                    'cost' : int(cost),
                    'fromline' : other_station['line'][0]
                })

                time.sleep(random.randint(1, 2))

    # Merge the stations with the same id
    merged_stations = []
    for station in stations:
        if station['id'] in [s['id'] for s in merged_stations]:
            for s in merged_stations:
                if s['id'] == station['id']:
                    s['line'].append(station['line'][0])
                    s['line_code'].append(station['line_code'][0])
                    s['connections'] += station['connections']
                    break
        else:
            merged_stations.append(station)

            
    # write the data to a json file
    # the json file contain chinese words, so we need to set ensure_ascii to False
    with open(os.path.join('..', 'clean', 'stations.json'), 'w', encoding='utf-8') as f:
        json.dump(merged_stations, f, ensure_ascii=False , indent=4)


if __name__ == "__main__":
    clean_data()
