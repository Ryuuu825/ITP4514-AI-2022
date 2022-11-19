import json

# get the station data
with open('data/clean/stations.json', encoding='utf-8') as file:
    file_contents = file.read()

# get the stations of lines
with open('data/clean/LineStations.json', encoding='utf-8') as file:
    line_contents = file.read()

# get the heuristic data
with open('data/clean/nodes_heuristic.json', encoding='utf-8') as file:
    heuristic_contents = file.read()

heuristics = json.loads(heuristic_contents)
data = json.loads(file_contents)
lines = json.loads(line_contents)
airportLine = {'56': "AsiaWorld-Expo", '47': "Airport",
               '46': "Tsing Yi", '45': "Kowloon", '44': "Hong Kong"}
# airportLine = ['56', '47', '42', '40', '39']
# store the stations key and value
stations = dict()
for i in data:
    stations[str(i['id'])] = i['name']

# make graph
# ['station1', 'station2', 'cost', 'current_line']
graph = []
for i in data:
    for j in i['connections']:
        graph.append([str(i['id']), str(j['id']), j['cost'], j['fromline']])

# estimate the cost of waiting for the next train in different lines
expectWaitTime = {
    "Airport Express": 0,
    "Disneyland Resort Line": 0,
    "East Rail Line": 2,
    "Island Line": 1,
    "Kwun Tong Line": 1,
    "Tuen Ma Line": 2,
    "Tung Chung Line": 3,
    "Tseung Kwan O Line": 1,
    "South Island Line": 2,
    "Tsuen Wan Line": 1
}

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