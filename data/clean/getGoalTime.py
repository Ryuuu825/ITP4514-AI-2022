import requests
import time
import json
import bs4

# get the station data
with open('data/clean/stations.json', encoding='utf-8') as file:
    file_contents = file.read()

# get the stations of lines
with open('data/clean/LineStations.json', encoding='utf-8') as file:
    line_contents = file.read()
data = json.loads(file_contents)
lines = json.loads(line_contents)
airportLine = {'56': "AsiaWorld-Expo", '47': "Airport",
               '46': "Tsing Yi", '45': "Kowloon", '44': "Hong Kong"}
# store the stations key and value
stations = dict()
for i in data:
    stations[str(i['id'])] = i['name']
    
# make graph
# ['station1', 'station2', 'cost', 'current_line']
# estimate the cost of waiting for the next train is 2 minutes
# the cost of data had been calculated with the cost of waiting for the next train, so we need to minus 2 minutes
graph = []
for i in data:
    for j in i['connections']:
        graph.append([str(i['id']), str(j['id']), j['cost']-1.3, j['fromline']])

# store the lines of stations
node_lines = dict()
for i in data:
    node_lines[str(i['id'])] = i['line']

# store the time of changing line in a station
change_lines_time = dict()
for i in data:
    try:
        change_lines_time[str(i['id'])] = i['walkingTime']
    except KeyError:
        pass

# clean the graph and get the nodes
temp = []
temp1 = []
totalcost = 0
for i in graph:
    temp.append(i[0])
    temp1.append(i[1])
nodes = set(temp).union(set(temp1))
nodes.remove("46")
nodes.remove("45")
nodes.remove("44")
stations = []
for i in nodes:
		stations.append(int(i))
stations.sort()
heuristic = dict()
# r = requests.get("https://www.mtr.com.hk/share/customer/jp/api/HRRoutes/?lang=C&"+"o=" + str(20) + "&d=" + str(30))
# list_of_dicts = r.content
# soup = bs4.BeautifulSoup(r.content, "html.parser")
# temp = json.loads(soup.text)
# heuristic["30"] = ["20", temp["routes"][0]["time"]]
result = []
d = []
for endnode in stations:
	ns = stations.copy()
	ns.remove(endnode)
	d = []
	for node in ns:
		r = requests.get("https://www.mtr.com.hk/share/customer/jp/api/HRRoutes/?lang=C&"+"o=" + str(endnode) + "&d=" + str(node))
		print(endnode, d, r.status_code)
		list_of_dicts = r.content
		soup = bs4.BeautifulSoup(r.content, "html.parser")
		temp = json.loads(soup.text)
		result.append(temp)
		d.append([node, temp["routes"][0]["time"]])
		time.sleep(0.1)
	heuristic[endnode] = d

with open('heuristic.json', 'w') as f:
    json.dump(heuristic, f, indent=4)

with open('data.json', 'w') as f:
    json.dump(result, f, indent=4)