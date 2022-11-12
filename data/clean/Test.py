# get the id of the by the station english name
import os
import json
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

with open(os.path.join('..', 'clean', 'stations.json'), 'r') as f:
    data = json.load(f)

def get_id(name):
    for station in data:
        if station['name'] == name:
            return station['id']
    return -1

# ChangeLine.txt
"""
To Kwa Wan > Whampoa

Mong Kok East > East Tsim Sha Tsui

"""

with open('ChangeLine.txt', 'r') as f:
    lines = f.readlines()

write_data = []

for line in lines:
    line = line.strip().split(' > ')
    o = get_id(line[0])
    d = get_id(line[1])

    url = base_url + "o=" + str(o) + "&d=" + str(d)
    driver.get(url)
    time.sleep(1)
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    temp = json.loads(soup.text)
    temp = temp['routes'][0]
    walking_time = temp['walkingTime']
    print(line[0], " -> " , line[1], " --- " , temp)

    for node in temp['path']:
        if node['linkType'] == 'INTERCHANGE':
            write_data.append({
                'ID' : node['ID'],
                'time' : node['time'],
            })

with open('ChangeLine.json', 'w') as f:
    json.dump(write_data, f, indent=4)


    






